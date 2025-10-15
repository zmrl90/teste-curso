import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

st.set_page_config(page_title="Gerador de Card de Viagem", layout="centered")

st.title("🌴 Gerador de Card de Viagem")

# Inputs do utilizador
titulo = st.text_input("Título da viagem", "Maldivas - Paraíso na Terra")
preco = st.text_input("Preço", "Desde 1.299€")
datas = st.text_input("Datas", "10 a 17 de Novembro")
hotel = st.text_input("Hotel", "Sun Siyam Iru Fushi 5⭐")
imagem_bg = st.text_input(
    "URL da imagem de fundo", 
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
)

# Fonte (usa Arial, ou fallback caso não exista)
try:
    fonte_titulo = ImageFont.truetype("arial.ttf", 80)
    fonte_info = ImageFont.truetype("arial.ttf", 50)
except:
    fonte_titulo = ImageFont.load_default()
    fonte_info = ImageFont.load_default()

# Função para centralizar texto com textbbox
def centralizar_texto(draw, texto, fonte, y, largura, cor=(255, 255, 255)):
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    w = bbox[2] - bbox[0]
    draw.text(((largura - w) / 2, y), texto, fill=cor, font=fonte)

# Botão para gerar imagem
if st.button("Gerar Card"):
    try:
        # Abrir imagem de fundo a partir da URL
        response = requests.get(imagem_bg)
        response.raise_for_status()
        bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        bg_img = bg_img.resize((1080, 1350))  # formato feed (4:5)

        largura, altura = bg_img.size

        # Criar overlay semitransparente na parte inferior
        overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        draw_overlay.rectangle([(0, altura - 450), (largura, altura)], fill=(0, 0, 0, 140))
        bg_img = Image.alpha_composite(bg_img, overlay)

        draw = ImageDraw.Draw(bg_img)

        # Adicionar texto
        centralizar_texto(draw, titulo, fonte_titulo, altura - 400, largura)
        centralizar_texto(draw, preco, fonte_info, altura - 270, largura)
        centralizar_texto(draw, datas, fonte_info, altura - 190, largura)
        centralizar_texto(draw, hotel, fonte_info, altura - 110, largura)

        # Mostrar imagem final
        st.image(bg_img, caption="Pré-visualização do teu card", use_container_width=True)

        # Converter imagem para bytes e preparar download
        buf = io.BytesIO()
        bg_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="⬇️ Fazer download do card",
            data=byte_im,
            file_name="card_viagem.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar a imagem: {e}")


