import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags
import requests
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# --------------------
# URLs de fontes (CDN)
# --------------------
FONT_SOURCES = {
    "regular": [
        "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-Regular.ttf",
        "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat-Regular.ttf",
    ],
    "semibold": [
        "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-SemiBold.ttf",
        "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat-SemiBold.ttf",
    ],
    "bold": [
        "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-Bold.ttf",
        "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat-Bold.ttf",
    ],
}

# --------------------
# Helpers
# --------------------
@st.cache_data(show_spinner=False)
def download_bytes(url, timeout=12):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.content
    except Exception:
        return None

def try_load_truetype_from_urls(url_list, size):
    for url in url_list:
        data = download_bytes(url)
        if data:
            try:
                return ImageFont.truetype(BytesIO(data), size=size)
            except Exception:
                continue
    return None  # sem fallback bitmap

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered(draw, text, font, x_center, y, fill=(255, 255, 255),
                  align="center", stroke_width=0, stroke_fill=(0, 0, 0)):
    w, h = text_size(draw, text, font)
    draw.text((x_center - w / 2, y), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)
    return w, h

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    try:
        exif = img._getexif()
        if not exif:
            return img
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                o = exif.get(orientation, None)
                if o == 3:  return img.rotate(180, expand=True)
                if o == 6:  return img.rotate(270, expand=True)
                if o == 8:  return img.rotate(90, expand=True)
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

def fit_font_to_block(draw, text, font_urls, target_height, max_width, min_size=40, max_size=400):
    lo, hi = min_size, max_size
    best = try_load_truetype_from_urls(font_urls, lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        f = try_load_truetype_from_urls(font_urls, mid)
        if f is None:
            break
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

        st.write("---")
        scale = st.slider("🅰️ Tamanho do texto (escala global)", 0.8, 3.0, 2.0, 0.1)

    submit = st.form_submit_button("🎨 Gerar e Pré-visualizar")

# --------------------
# Render
# --------------------
if submit:
    if fmt == "Feed 1080×1350":
        W, H = 1080, 1350
    elif fmt == "Quadrado 1080×1080":
        W, H = 1080, 1080
    elif fmt == "Wide 1920×1080":
        W, H = 1920, 1080
    else:
        W, H = 1080, 1920

    # Carregar imagem
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
        st.error(f"Erro ao carregar imagem: {e}")
        st.stop()

    bg = cover_resize(bg, W, H)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    canvas = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(canvas)
    accent_rgb = tuple(int(color_accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # Fontes
    f_top   = try_load_truetype_from_urls(FONT_SOURCES["regular"], int(34 * scale))
    f_sub   = try_load_truetype_from_urls(FONT_SOURCES["semibold"], int(54 * scale))
    f_price = try_load_truetype_from_urls(FONT_SOURCES["bold"], int(360 * scale))
    f_plab  = try_load_truetype_from_urls(FONT_SOURCES["semibold"], int(72 * scale))
    f_pby   = try_load_truetype_from_urls(FONT_SOURCES["regular"], int(60 * scale))
    f_icon  = try_load_truetype_from_urls(FONT_SOURCES["regular"], int(58 * scale))
    f_emoji = try_load_truetype_from_urls(FONT_SOURCES["semibold"], int(86 * scale))
    f_foot  = try_load_truetype_from_urls(FONT_SOURCES["regular"], int(40 * scale))

    required_fonts = [f_top, f_sub, f_price, f_plab, f_pby, f_icon, f_emoji, f_foot]
    if any(f is None for f in required_fonts):
        st.error("❌ Não consegui carregar as fontes Montserrat. Verifica a tua ligação à internet e tenta novamente.")
        st.stop()

    # Topo
    top_y = int(28 * scale)
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", f_top, W // 2, top_y)
    draw_centered(draw, "iCliGo travel consultant", f_top, W // 2, top_y + int(48 * scale))

    # Subtítulo
    subtitle_y = 260 if fmt == "Feed 1080×1350" else (220 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 360)
    subtitle_wrapped = "\n".join(textwrap.wrap(subtitle.upper(), width=38))
    draw_centered(draw, subtitle_wrapped, f_sub, W // 2, subtitle_y,
                  fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))

    # DESTINO
    dest_text = destination.upper()
    block_height = 200
    block_top = 380 if fmt == "Feed 1080×1350" else (320 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 520)
    block_center_y = block_top + block_height // 2
    f_dest = fit_font_to_block(draw, dest_text, FONT_SOURCES["bold"], block_height, int(W * 0.9), min_size=80, max_size=420)
    if f_dest is None:
        st.error("❌ Falha ao carregar a fonte Montserrat-Bold.")
        st.stop()
    w_dest, h_dest = text_size(draw, dest_text, f_dest)
    dest_y = block_center_y - h_dest // 2
    draw.text((W/2 - w_dest/2, dest_y), dest_text, font=f_dest, fill=accent_rgb, stroke_width=3, stroke_fill=(0,0,0))

    # Preço
    price_cx = int(W * 0.72)
    price_top = 720 if fmt == "Feed 1080×1350" else (610 if fmt.startswith("Quadrado") else (560 if fmt.startswith("Wide") else 980))
    draw_centered(draw, price_label.upper(), f_plab, price_cx, price_top)
    _, hp = draw_centered(draw, price, f_price, price_cx, price_top + int(20 * scale),
                          fill=accent_rgb, stroke_width=3, stroke_fill=(0, 0, 0))
    draw_centered(draw, price_by.upper(), f_pby, price_cx,
                  price_top + int(20 * scale) + int(hp * 0.75))

    # Ícones
    icons_y = 1020 if fmt == "Feed 1080×1350" else (840 if fmt.startswith("Quadrado") else (860 if fmt.startswith("Wide") else 1460))
    icon_texts = [
        (f"{origin}\n{dates}", "✈️"),
        (f"HOTEL\n{hotel}", "🏨"),
        (meal, "🍽️"),
        (baggage, "🧳"),
        (transfer, "🚐"),
    ]
    spacing = W // len(icon_texts)
    for i, (txt, ic) in enumerate(icon_texts):
        xc = spacing * i + spacing // 2
        draw_centered(draw, ic, f_emoji, xc, icons_y - int(64 * scale), fill=accent_rgb)
        w_lbl, _ = text_size(draw, txt.upper(), f_icon)
        draw.multiline_text((xc - w_lbl/2, icons_y), txt.upper(), font=f_icon,
                            fill=(255, 255, 255), align="center",
                            spacing=int(8 * scale), stroke_width=2, stroke_fill=(0, 0, 0))

    # Rodapé
    footer_y = 1280 if fmt == "Feed 1080×1350" else (1000 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 1820)
    footer_text = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES."
    draw_centered(draw, footer_text, f_foot, W // 2, footer_y)

    # Preview e download
    st.markdown("### Pré-visualização")
    st.image(canvas.convert("RGB"), use_container_width=True)
    buf = BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    st.download_button("⬇️ Fazer download do card (PNG)", data=buf, file_name=outfile_name, mime="image/png")

    st.success("✅ Card gerado com sucesso — ajusta o slider de escala até ficar visualmente ideal.")
