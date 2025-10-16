import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# --------------------
# Helpers
# --------------------
def load_font(font_name, size, bold=False):
    """Carrega Arial (bold ou normal)."""
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        else:
            return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered(draw, text, font, x_center, y, fill=(255, 255, 255)):
    """Desenha texto centrado horizontalmente."""
    w, h = text_size(draw, text, font)
    draw.text((x_center - w / 2, y), text, font=font, fill=fill)
    return w, h

def fix_exif_orientation(img):
    try:
        exif = img._getexif()
        if not exif:
            return img
        for orientation, tag in ExifTags.TAGS.items():
            if tag == 'Orientation':
                val = exif.get(orientation, None)
                if val == 3:
                    return img.rotate(180, expand=True)
                elif val == 6:
                    return img.rotate(270, expand=True)
                elif val == 8:
                    return img.rotate(90, expand=True)
                break
    except Exception:
        pass
    return img

def cover_resize(img, target_w, target_h):
    """Redimensiona a imagem para preencher o espaço mantendo proporção."""
    ratio_img = img.width / img.height
    ratio_tar = target_w / target_h
    if ratio_img > ratio_tar:
        new_h = target_h
        new_w = int(ratio_img * new_h)
    else:
        new_w = target_w
        new_h = int(new_w / ratio_img)
    img = img.resize((new_w, new_h))
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))

# --------------------
# UI
# --------------------
st.title("🧳 Gerador de Card de Viagem (Arial, sem contorno)")

with st.form("inputs"):
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Conteúdo do Card")
        subtitle = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta")
        destination = st.text_input("Destino (grande)", "NÁPOLES")
        price = st.text_input("Preço", "409€")
        price_label = st.text_input("Rótulo acima do preço", "DESDE")
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
        upload = st.file_uploader("Carrega uma imagem (jpg/png)", type=["jpg", "jpeg", "png"])
        fmt = st.selectbox("Formato", ("Feed 1080×1350", "Quadrado 1080×1080", "Wide 1920×1080", "Story 1080×1920"))
        outfile_name = st.text_input("Nome do ficheiro", "card_viagem.png")
        color_accent = st.color_picker("Cor de destaque (texto & ícones)", "#00ffae")
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

    if upload is None:
        st.error("⚠️ Carrega uma imagem de fundo primeiro.")
        st.stop()

    bg = fix_exif_orientation(Image.open(upload).convert("RGBA"))
    bg = cover_resize(bg, W, H)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    canvas = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(canvas)

    accent_rgb = tuple(int(color_accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # --------------------
    # Fontes (Arial)
    # --------------------
    f_top = load_font("arial", int(34 * scale))
    f_sub = load_font("arial", int(54 * scale))
    f_dest = load_font("arial", int(180 * scale), bold=True)
    f_price = load_font("arial", int(300 * scale), bold=True)
    f_plab = load_font("arial", int(72 * scale), bold=True)
    f_pby = load_font("arial", int(60 * scale))
    f_icon = load_font("arial", int(48 * scale))
    f_emoji = load_font("arial", int(80 * scale))
    f_foot = load_font("arial", int(40 * scale))

    # --------------------
    # Layout
    # --------------------
    top_y = int(28 * scale)
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", f_top, W // 2, top_y)
    draw_centered(draw, "iCliGo travel consultant", f_top, W // 2, top_y + int(48 * scale))

    subtitle_y = 260 if fmt == "Feed 1080×1350" else (220 if "Quadrado" in fmt or "Wide" in fmt else 360)
    draw_centered(draw, subtitle.upper(), f_sub, W // 2, subtitle_y)

    dest_y = 420 if fmt == "Feed 1080×1350" else (340 if "Quadrado" in fmt else 520)
    draw_centered(draw, destination.upper(), f_dest, W // 2, dest_y, fill=accent_rgb)

    price_cx = int(W * 0.72)
    price_top = 760 if fmt == "Feed 1080×1350" else (620 if "Quadrado" in fmt else 980)
    draw_centered(draw, price_label.upper(), f_plab, price_cx, price_top)
    _, hp = draw_centered(draw, price, f_price, price_cx, price_top + int(30 * scale), fill=accent_rgb)
    draw_centered(draw, price_by.upper(), f_pby, price_cx,
                  price_top + int(30 * scale) + int(hp * 0.8))

    icons_y = 1020 if fmt == "Feed 1080×1350" else (840 if "Quadrado" in fmt else 1460)
    icons = [
        (f"{origin}\n{dates}", "✈️"),
        (f"HOTEL\n{hotel}", "🏨"),
        (meal, "🍽️"),
        (baggage, "🧳"),
        (transfer, "🚐"),
    ]
    spacing = W // len(icons)
    for i, (txt, ic) in enumerate(icons):
        xc = spacing * i + spacing // 2
        draw_centered(draw, ic, f_emoji, xc, icons_y - int(64 * scale), fill=accent_rgb)
        draw.multiline_text(
            (xc - 100, icons_y), txt.upper(), font=f_icon, fill=(255, 255, 255),
            align="center", spacing=int(8 * scale)
        )

    footer_y = 1280 if fmt == "Feed 1080×1350" else (1000 if "Quadrado" in fmt else 1820)
    footer_text = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES."
    draw_centered(draw, footer_text, f_foot, W // 2, footer_y)

    # --------------------
    # Output
    # --------------------
    st.image(canvas.convert("RGB"), use_container_width=True)
    buf = BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    st.download_button("⬇️ Fazer download do card (PNG)", data=buf, file_name=outfile_name, mime="image/png")
    st.success("✅ Card gerado com sucesso — agora com Arial e sem contorno!")


