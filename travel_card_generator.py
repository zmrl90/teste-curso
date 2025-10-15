import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags
import requests
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# ---------- Funções auxiliares ----------
def fix_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception:
        pass
    return image

def draw_centered(draw, text, font, x, y, color):
    w, h = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text((x - w / 2, y), text, font=font, fill=color)

def wrap_text(draw, text, font, max_width):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        w, _ = draw.textbbox((0, 0), test_line, font=font)[2:]
        if w < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    return "\n".join(lines)

# ---------- Interface ----------
st.title("🧳 Gerador de Card de Viagem")

# Campos de input
col1, col2 = st.columns(2)

with col1:
    subtitulo = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta")
    destino = st.text_input("Destino", "NÁPOLES")
    preco = st.text_input("Preço", "409€")
    cidade = st.text_input("Cidade de Partida", "Porto")
    datas = st.text_input("Datas", "7 a 15 Março")
    hotel = st.text_input("Hotel", "Hotel Herculaneum")
    refeicao = st.text_input("Refeição", "Pequeno Almoço")
    bagagem = st.text_input("Bagagem", "Bagagem de mão")
    transfer = st.text_input("Transfer", "Transfer In + Out")

with col2:
    formato = st.selectbox("Formato", ["Feed 1080x1350", "Story 1080x1920", "Wide 1920x1080", "Quadrado 1080x1080"])
    cor = st.color_picker("Cor principal", "#00FFAE")
    image_file = st.file_uploader("📸 Upload da imagem de fundo", type=["jpg", "png", "jpeg"])

if st.button("🎨 Gerar Card"):
    # Tamanhos
    formatos = {
        "Feed 1080x1350": (1080, 1350),
        "Story 1080x1920": (1080, 1920),
        "Wide 1920x1080": (1920, 1080),
        "Quadrado 1080x1080": (1080, 1080)
    }
    W, H = formatos[formato]

    # Carregar imagem
    if image_file is None:
        st.error("Por favor, faz upload de uma imagem de fundo.")
        st.stop()

    bg = Image.open(image_file).convert("RGBA")
    bg = fix_image_orientation(bg)
    bg = bg.resize((W, H))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 110))
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    # Fonte Montserrat
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
        font_bold = ImageFont.truetype(BytesIO(requests.get(font_url).content), 120)
        font_regular = ImageFont.truetype(BytesIO(requests.get(font_url).content), 40)
        font_small = ImageFont.truetype(BytesIO(requests.get(font_url).content), 30)
    except Exception:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Topo
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", font_small, W // 2, 40, (255, 255, 255))
    draw_centered(draw, "iCliGo travel consultant", font_small, W // 2, 80, (255, 255, 255))

    # Subtítulo
    texto_subtitulo = wrap_text(draw, subtitulo.upper(), font_small, W - 200)
    draw.multiline_text((W // 2 - 400, H * 0.22), texto_subtitulo, fill=(255, 255, 255), font=font_small, align="center")

    # Destino
    draw_centered(draw, destino.upper(), font_bold, W // 2, int(H * 0.30), tuple(int(cor.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))

    # Preço
    draw_centered(draw, "DESDE", font_small, W // 2, int(H * 0.48), (255, 255, 255))
    draw_centered(draw, preco, font_bold.font_variant(size=160), W // 2, int(H * 0.52), tuple(int(cor.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
    draw_centered(draw, "POR PESSOA", font_small, W // 2, int(H * 0.67), (255, 255, 255))

    # Ícones
    icons = ["✈️", "🏨", "🍽️", "🧳", "🚐"]
    texts = [
        f"{cidade}\n{datas}",
        f"HOTEL\n{hotel}",
        refeicao,
        bagagem,
        transfer
    ]
    y_icons = int(H * 0.78)
    for i in range(5):
        x = int(W * (i + 0.5) / 5)
        draw_centered(draw, icons[i], font_regular.font_variant(size=80), x, y_icons, tuple(int(cor.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
        draw.multiline_text((x - 120, y_icons + 80), texts[i].upper(), fill=(255, 255, 255), font=font_small, align="center")

    # Rodapé
    draw_centered(draw, "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES.", font_small, W // 2, H - 60, (255, 255, 255))

    # Mostrar e permitir download
    st.image(bg, caption="Pré-visualização do Card", use_container_width=True)

    buf = BytesIO()
    bg.convert("RGB").save(buf, format="PNG")
    st.download_button(
        label="⬇️ Fazer download do card",
        data=buf.getvalue(),
        file_name=f"card_{destino.lower()}.png",
        mime="image/png"
    )


