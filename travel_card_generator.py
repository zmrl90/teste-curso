import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# --------------------
# Helpers
# --------------------
FONT_URLS = {
    "regular": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Regular.ttf",
    "semibold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-SemiBold.ttf",
    "bold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf",
}

def download_font(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return BytesIO(r.content)
    except Exception:
        return None

def load_fonts():
    # try to download fonts; fallback to default
    f_reg = download_font(FONT_URLS["regular"])
    f_sem = download_font(FONT_URLS["semibold"])
    f_bold = download_font(FONT_URLS["bold"])
    fonts = {}
    try:
        fonts["reg"] = ImageFont.truetype(f_reg if f_reg else BytesIO(), size=48)
    except Exception:
        fonts["reg"] = ImageFont.load_default()
    try:
        fonts["sem"] = ImageFont.truetype(f_sem if f_sem else BytesIO(), size=40)
    except Exception:
        fonts["sem"] = ImageFont.load_default()
    try:
        fonts["bold"] = ImageFont.truetype(f_bold if f_bold else BytesIO(), size=120)
    except Exception:
        fonts["bold"] = ImageFont.load_default()
    return fonts

def text_size(draw, text, font):
    # returns width, height using textbbox to be Pillow-version-safe
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return w, h

def draw_centered(draw, text, font, x_center, y, fill=(255,255,255), align="center"):
    # For multiline use draw.multiline_text with computed starting x
    if "\n" in text or isinstance(text, list):
        if isinstance(text, list):
            text = "\n".join(text)
        lines = text.split("\n")
        # compute width of widest line
        widths = [text_size(draw, line, font)[0] for line in lines]
        max_w = max(widths)
        start_x = x_center - max_w/2
        draw.multiline_text((start_x, y), text, font=font, fill=fill, align=align, spacing=6)
        return max_w, sum(text_size(draw, line, font)[1] for line in lines) + (len(lines)-1)*6
    else:
        w,h = text_size(draw, text, font)
        draw.text((x_center - w/2, y), text, font=font, fill=fill)
        return w,h

# --------------------
# UI
# --------------------
st.title("🧳 Gerador de Card de Viagem (template: NÁPOLES)")

with st.form("inputs"):
    col_a, col_b = st.columns([2,1])

    with col_a:
        st.subheader("Conteúdo do Card")
        subtitle = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta")
        destination = st.text_input("Destino (grande)", "NÁPOLES")
        price = st.text_input("Preço", "409€")
        price_label = st.text_input("Preço - rótulo acima (ex: Desde)", "DESDE")
        price_by = st.text_input("Texto abaixo do preço", "POR PESSOA")

        st.write("---")
        st.write("Detalhes (linha de ícones)")
        origin = st.text_input("Cidade de Partida", "Porto")
        dates = st.text_input("Datas", "7 a 15 Março")
        hotel = st.text_input("Hotel", "Hotel Herculaneum")
        meal = st.text_input("Regime", "Pequeno Almoço")
        baggage = st.text_input("Bagagem", "Bagagem de mão")
        transfer = st.text_input("Transfer", "Transfer In + Out")

    with col_b:
        st.subheader("Imagem e formato")
        input_mode = st.radio("Fonte da imagem de fundo", ("Upload local", "URL"), index=0)
        if input_mode == "Upload local":
            upload = st.file_uploader("Carrega uma imagem (jpg/png)", type=["jpg", "jpeg", "png"])
            image_url = ""
        else:
            upload = None
            image_url = st.text_input("URL da imagem", "https://www.melhoresdestinos.com.br/wp-content/uploads/2020/12/quanto-custa-viajar-maldivas-capa2019-01.jpg")

        st.write("---")
        fmt = st.selectbox("Formato da imagem", ("Feed 1080×1350", "Quadrado 1080×1080", "Wide 1920×1080", "Story 1080×1920"), index=0)
        outfile_name = st.text_input("Nome do ficheiro para download", "card_viagem.png")
        color_accent = st.color_picker("Cor de destaque (texto & ícones)", "#00ffae")

    submit = st.form_submit_button("🎨 Gerar e Pré-visualizar")

# --------------------
# Process & Render
# --------------------
if submit:
    # determine size
    if fmt == "Feed 1080×1350":
        W, H = 1080, 1350
    elif fmt == "Quadrado 1080×1080":
        W, H = 1080, 1080
    elif fmt == "Wide 1920×1080":
        W, H = 1920, 1080
    else:  # Story
        W, H = 1080, 1920

    # load background image (upload or url)
    try:
        if upload is not None:
            bg = Image.open(upload).convert("RGBA")
        else:
            resp = requests.get(image_url, timeout=15)
            resp.raise_for_status()
            bg = Image.open(BytesIO(resp.content)).convert("RGBA")
    except Exception as e:
        st.error(f"Erro ao carregar imagem de fundo: {e}")
        st.stop()

    # resize and crop-ish to fill box (cover)
    bg_ratio = bg.width / bg.height
    target_ratio = W / H
    if bg_ratio > target_ratio:
        # bg is wider -> crop sides
        new_h = H
        new_w = int(bg_ratio * new_h)
    else:
        # bg is taller -> crop top/bottom
        new_w = W
        new_h = int(new_w / bg_ratio)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)

    # center crop to W x H
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    bg = bg.crop((left, top, left + W, top + H))

    # apply overlay (darker)
    overlay = Image.new("RGBA", (W, H), (0,0,0,120))
    canvas = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(canvas)

    # load fonts (with sizes tuned for canvas)
    fonts_stream = load_fonts()

    # choose sizes proportional to W/H
    # Big title size
    big_size = max(72, int(W * 0.24))  # adjust
    mid_size = max(20, int(W * 0.035))
    small_size = max(14, int(W * 0.025))
    price_big = max(64, int(W * 0.18))

    # try to re-create fonts with sizes
    try:
        f_bold = ImageFont.truetype(BytesIO(requests.get(FONT_URLS["bold"]).content), size=big_size)
        f_sem = ImageFont.truetype(BytesIO(requests.get(FONT_URLS["semibold"]).content), size=mid_size)
        f_reg = ImageFont.truetype(BytesIO(requests.get(FONT_URLS["regular"]).content), size=small_size)
        f_price = ImageFont.truetype(BytesIO(requests.get(FONT_URLS["bold"]).content), size=price_big)
        f_price_label = ImageFont.truetype(BytesIO(requests.get(FONT_URLS["semibold"]).content), size=int(price_big*0.18))
    except Exception:
        # fallback
        f_bold = fonts_stream["bold"]
        f_sem = fonts_stream["sem"]
        f_reg = fonts_stream["reg"]
        f_price = fonts_stream["bold"]
        f_price_label = fonts_stream["sem"]

    accent_rgb = tuple(int(color_accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # TOP texts (fixed)
    top_y = int(H * 0.03)
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", f_reg, W//2, top_y, fill=(255,255,255))
    draw_centered(draw, "iCliGo travel consultant", f_reg, W//2, top_y + int(small_size*1.6), fill=(255,255,255))

    # SUBTITLE ~ above big title (slightly higher)
    subtitle_y = int(H * 0.22)
    # wrap subtitle to width
    subtitle_wrapped = "\n".join(textwrap.wrap(subtitle.upper(), width=40))
    draw_centered(draw, subtitle_wrapped, f_reg, W//2, subtitle_y, fill=(255,255,255))

    # BIG TITLE (destination) centered roughly 1/3 down
    title_y = int(H * 0.30)
    # ensure uppercase and not too long
    dest_text = destination.upper()
    draw_centered(draw, dest_text, f_bold, W//2, title_y, fill=accent_rgb)

    # PRICE block (placed to right-ish or centered depending space)
    price_label_y = int(H * 0.52)
    draw_centered(draw, price_label.upper(), f_price_label, int(W*0.72), price_label_y, fill=(255,255,255))
    draw_centered(draw, price, f_price, int(W*0.72), price_label_y + int(price_big*0.05), fill=accent_rgb)
    draw_centered(draw, price_by.upper(), f_reg, int(W*0.72), price_label_y + int(price_big*0.25), fill=(255,255,255))

    # ICONS row near bottom
    icons_y = int(H * 0.78)
    # evenly spaced across width
    n = 5
    spacing = W // n
    icon_texts = [
        (f"{origin}\n{dates}", "✈️"),
        (f"HOTEL\n{hotel}", "🏨"),
        (meal, "🍽️"),
        (baggage, "🧳"),
        (transfer, "🚐"),
    ]
    for i, (txt, ic) in enumerate(icon_texts):
        x_center = spacing * i + spacing//2
        # draw icon
        try:
            # use semibold for icon to be slightly larger
            draw_centered(draw, ic, f_sem, x_center, icons_y - int(mid_size*1.2), fill=accent_rgb)
        except Exception:
            draw_centered(draw, ic, f_reg, x_center, icons_y - int(mid_size*1.2), fill=accent_rgb)
        # draw label below icon (multiple lines)
        lines = txt.upper()
        draw.multiline_text((x_center -  (text_size(draw, lines, f_reg)[0]/2), icons_y + 10), lines, font=f_reg, fill=(255,255,255), align="center", spacing=6)

    # footer small line
    footer_y = H - int(small_size * 2.5)
    footer_text = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES."
    draw_centered(draw, footer_text, f_reg, W//2, footer_y, fill=(255,255,255))

    # Show preview
    st.markdown("### Pré-visualização")
    st.image(canvas.convert("RGB"), use_container_width=True)

    # prepare buffer for download
    buf = BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)

    st.download_button(
        label="⬇️ Fazer download do card (PNG)",
        data=buf,
        file_name=outfile_name or "card_viagem.png",
        mime="image/png"
    )

    st.success("Gerado com sucesso — descarrega o PNG ou ajusta campos e gera de novo.")



