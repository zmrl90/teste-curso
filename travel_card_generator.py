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
imagem_bg = st.text_input("URL da imagem de fundo", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e")

# Fonte padrão (usa Arial do sistema)
try:
    fonte_titulo = ImageFont.truetype("arial.ttf", 80)
    fonte_info = ImageFont.truetype("arial.ttf", 50)
except:
    fonte_titulo = ImageFont.load_default()
    fonte_info = ImageFont.load_default()

# Botão para gerar imagem
if st.button("Gerar Card"):
    try:
        # Tenta abrir imagem de fundo
        response = requests.get(imagem_bg)
        response.raise_for_status()
        bg_img = Image.open(io.BytesIO(response.content)).convert("RGB")
        bg_img = bg_img.resize((1080, 1350))  # formato de post de feed

        draw = ImageDraw.Draw(bg_img)
        largura, altura = bg_img.size

        # Caixa semitransparente no fundo do texto
        overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        draw_overlay.rectangle([(0, altura - 450), (largura, altura)], fill=(0, 0, 0, 140))
        bg_img = Image.alpha_composite(bg_img.convert("RGBA"), overlay)

        draw = ImageDraw.Draw(bg_img)

        # Função auxiliar para centralizar texto
        def centralizar_texto(texto, fonte, y, cor=(255, 255, 255)):
            w, h = draw.textsize(texto, font=fonte)
            draw.text(((largura - w) / 2, y), texto, fill=cor, font=fonte)

        # Escrever texto
        centralizar_texto(titulo, fonte_titulo, altura - 400)
        centralizar_texto(preco, fonte_info, altura - 270)
        centralizar_texto(datas, fonte_info, altura - 190)
        centralizar_texto(hotel, fonte_info, altura - 110)

        # Mostrar resultado
        st.image(bg_img, caption="Pré-visualização do teu card", use_container_width=True)

        # Converter para bytes e preparar download
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


