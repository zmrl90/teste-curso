import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags
import requests
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# --------------------
# Constantes / Fontes
# --------------------
FONT_URLS = {
    "regular": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Regular.ttf",
    "semibold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-SemiBold.ttf",
    "bold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf",
}

# --------------------
# Helpers
# --------------------
def download_bytes(url, timeout=12):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.content
    except Exception:
        return None

def safe_truetype_from_url(url, size):
    data = download_bytes(url)
    if data:
        try:
            return ImageFont.truetype(BytesIO(data), size=size)
        except Exception:
            pass
    return ImageFont.load_default()

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered(draw, text, font, x_center, y, fill=(255, 255, 255), align="center"):
    w, h = text_size(draw, text, font)
    draw.text((x_center - w / 2, y), text, font=font, fill=fill)
    return w, h

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    try:
        exif = img._getexif()
        if not exif:
            return img
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                o = exif.get(orientation, None)
                if o == 3:
                    return img.rotate(180, expand=True)
                elif o == 6:
                    return img.rotate(270, expand=True)
                elif o == 8:
                    return img.rotate(90, expand=True)
                break
    except Exception:
        pass
    return img

def cover_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    ratio_img = img.width / img.height
    ratio_tar = target_w / target_h
    if ratio_img > ratio_tar:
        new_h = target_h
        new_w = int(ratio_img * new_h)
    else:
        new_w = target_w
        new_h = int(new_w / ratio_img)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))

def fit_font_to_block(draw, text, url_bold, target_height, max_width, min_size=40, max_size=600):
    lo, hi = min_size, max_size
    best = safe_truetype_from_url(url_bold, lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        f = safe_truetype_from_url(url_bold, mid)
        w, h = text_size(draw, text, f)
        if h <= target_height and w <= max_width:
            best = f
            lo = mid + 1
        else:
            hi = mid - 1
    return best

# --------------------
# UI
# --------------------
st.title("🧳 Gerador de Card de Viagem (template: NÁPOLES)")

with st.form("inputs"):
    col_a, col_b = st.columns([2, 1])

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
            image_url = st.text_input(
                "URL da imagem",
                "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1400&auto=format&fit=crop"
            )

        st.write("---")
        fmt = st.selectbox("Formato da imagem", ("Feed 1080×1350", "Quadrado 1080×1080", "Wide 1920×1080", "Story 1080×1920"), index=0)
        outfile_name = st.text_input("Nome do ficheiro para download", "card_viagem.png")
        color_accent = st.color_picker("Cor de destaque (texto & ícones)", "#00ffae")

    submit = st.form_submit_button("🎨 Gerar e Pré-visualizar")

# --------------------
# Render
# --------------------
if submit:
    # Tamanho por formato
    if fmt == "Feed 1080×1350":
        W, H = 1080, 1350
    elif fmt == "Quadrado 1080×1080":
        W, H = 1080, 1080
    elif fmt == "Wide 1920×1080":
        W, H = 1920, 1080
    else:
        W, H = 1080, 1920

    # Carregar fundo
    try:
        if upload is not None:
            bg = Image.open(upload)
        else:
            data = download_bytes(image_url, timeout=15)
            if not data:
                raise RuntimeError("Falha ao fazer download da imagem.")
            bg = Image.open(BytesIO(data))
        bg = fix_exif_orientation(bg).convert("RGBA")
    except Exception as e:
        st.error(f"Erro ao carregar imagem de fundo: {e}")
        st.stop()

    # Ajustar imagem (cover)
    bg = cover_resize(bg, W, H)

    # Overlay escuro e base do desenho
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 90))
    canvas = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(canvas)

    # Cor de destaque
    accent_rgb = tuple(int(color_accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # Fontes baseadas no template - TAMANHOS GRANDES
    if fmt == "Feed 1080×1350":
        f_top = safe_truetype_from_url(FONT_URLS["regular"], 32)
        f_sub = safe_truetype_from_url(FONT_URLS["regular"], 48)
        f_price = safe_truetype_from_url(FONT_URLS["bold"], 200)
        f_plab = safe_truetype_from_url(FONT_URLS["semibold"], 42)
        f_pby = safe_truetype_from_url(FONT_URLS["regular"], 38)
        f_icon = safe_truetype_from_url(FONT_URLS["semibold"], 36)
        f_icon_emoji = safe_truetype_from_url(FONT_URLS["semibold"], 80)
        f_foot = safe_truetype_from_url(FONT_URLS["regular"], 28)
        dest_min, dest_max = 200, 450
    elif fmt == "Quadrado 1080×1080":
        f_top = safe_truetype_from_url(FONT_URLS["regular"], 30)
        f_sub = safe_truetype_from_url(FONT_URLS["regular"], 44)
        f_price = safe_truetype_from_url(FONT_URLS["bold"], 180)
        f_plab = safe_truetype_from_url(FONT_URLS["semibold"], 38)
        f_pby = safe_truetype_from_url(FONT_URLS["regular"], 34)
        f_icon = safe_truetype_from_url(FONT_URLS["semibold"], 32)
        f_icon_emoji = safe_truetype_from_url(FONT_URLS["semibold"], 70)
        f_foot = safe_truetype_from_url(FONT_URLS["regular"], 26)
        dest_min, dest_max = 180, 400
    elif fmt == "Wide 1920×1080":
        f_top = safe_truetype_from_url(FONT_URLS["regular"], 36)
        f_sub = safe_truetype_from_url(FONT_URLS["regular"], 52)
        f_price = safe_truetype_from_url(FONT_URLS["bold"], 220)
        f_plab = safe_truetype_from_url(FONT_URLS["semibold"], 46)
        f_pby = safe_truetype_from_url(FONT_URLS["regular"], 42)
        f_icon = safe_truetype_from_url(FONT_URLS["semibold"], 38)
        f_icon_emoji = safe_truetype_from_url(FONT_URLS["semibold"], 85)
        f_foot = safe_truetype_from_url(FONT_URLS["regular"], 30)
        dest_min, dest_max = 220, 480
    else:  # Story 1080×1920
        f_top = safe_truetype_from_url(FONT_URLS["regular"], 38)
        f_sub = safe_truetype_from_url(FONT_URLS["regular"], 56)
        f_price = safe_truetype_from_url(FONT_URLS["bold"], 240)
        f_plab = safe_truetype_from_url(FONT_URLS["semibold"], 50)
        f_pby = safe_truetype_from_url(FONT_URLS["regular"], 44)
        f_icon = safe_truetype_from_url(FONT_URLS["semibold"], 40)
        f_icon_emoji = safe_truetype_from_url(FONT_URLS["semibold"], 90)
        f_foot = safe_truetype_from_url(FONT_URLS["regular"], 32)
        dest_min, dest_max = 240, 520

    # Topo
    top_y = 50
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", f_top, W // 2, top_y, fill=(255, 255, 255))
    draw_centered(draw, "iCliGo travel consultant", f_top, W // 2, top_y + 50, fill=(255, 255, 255))

    # Subtítulo - ajustar posição baseado no template
    subtitle_y = 240 if fmt == "Feed 1080×1350" else (200 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 340)
    subtitle_wrapped = "\n".join(textwrap.wrap(subtitle.upper(), width=40))
    draw_centered(draw, subtitle_wrapped, f_sub, W // 2, subtitle_y, fill=(255, 255, 255))

    # DESTINO (auto-fit) - o texto mais importante
    dest_text = destination.upper()
    block_height = 350  # Aumentado significativamente
    block_top = 360 if fmt == "Feed 1080×1350" else (300 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 500)
    block_center_y = block_top + block_height // 2
    f_dest = fit_font_to_block(draw, dest_text, FONT_URLS["bold"], target_height=block_height, max_width=int(W * 0.95), min_size=dest_min, max_size=dest_max)
    w_dest, h_dest = text_size(draw, dest_text, f_dest)
    dest_y = block_center_y - h_dest // 2
    draw.text((W/2 - w_dest/2, dest_y), dest_text, font=f_dest, fill=accent_rgb)

    # Preço
    price_cx = int(W * 0.75)
    price_top = 800 if fmt == "Feed 1080×1350" else (680 if fmt.startswith("Quadrado") else (620 if fmt.startswith("Wide") else 1080))
    draw_centered(draw, price_label.upper(), f_plab, price_cx, price_top, fill=(255, 255, 255))
    _, hp = draw_centered(draw, price, f_price, price_cx, price_top + 60, fill=accent_rgb)
    draw_centered(draw, price_by.upper(), f_pby, price_cx, price_top + 60 + int(hp * 0.9), fill=(255, 255, 255))

    # Ícones / detalhes
    icons_y = 1120 if fmt == "Feed 1080×1350" else (920 if fmt.startswith("Quadrado") else (920 if fmt.startswith("Wide") else 1600))
    icon_texts = [
        (f"{origin}\n{dates}", "✈"),
        (f"HOTEL\n{hotel}", "🏨"),
        (meal, "🍽"),
        (baggage, "💼"),
        (transfer, "🚐"),
    ]
    n = len(icon_texts)
    spacing = W // n
    for i, (txt, ic) in enumerate(icon_texts):
        xc = spacing * i + spacing // 2
        draw_centered(draw, ic, f_icon_emoji, xc, icons_y - 100, fill=accent_rgb)
        lines = txt.upper()
        w_lbl, _ = text_size(draw, lines, f_icon)
        draw.multiline_text((xc - w_lbl/2, icons_y), lines, font=f_icon, fill=(255, 255, 255), align="center", spacing=4)

    # Rodapé
    footer_y = 1290 if fmt == "Feed 1080×1350" else (1020 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 1850)
    footer_text = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES."
    draw_centered(draw, footer_text, f_foot, W // 2, footer_y, fill=(255, 255, 255))

    # Preview e download
    st.markdown("### Pré-visualização")
    st.image(canvas.convert("RGB"), use_container_width=True)

    buf = BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    st.download_button("⬇️ Fazer download do card (PNG)", data=buf, file_name=outfile_name or "card_viagem.png", mime="image/png")

    st.success("✅ Card gerado - Layout baseado no template!