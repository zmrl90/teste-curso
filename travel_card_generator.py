import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

st.set_page_config(page_title="Gerador de Card de Viagem", layout="centered")

st.title("🌴 Gerador de Card de Viagem")

# --- Escolher formato ---
formato = st.selectbox(
    "Escolhe o formato do card:",
    ["Feed (1080x1350)", "Story (1080x1920)", "Wide (1920x1080)"]
)

if formato == "Feed (1080x1350)":
    largura, altura = 1080, 1350
elif formato == "Story (1080x1920)":
    largura, altura = 1080, 1920
else:
    largura, altura = 1920, 1080

# --- Inputs principais ---
st.markdown("### 🧭 Dados do destino")
subtitulo = st.text_input(
    "Subtítulo", 
    "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta"
)
destino = st.text_input("Destino", "NÁPOLES")
preco = st.text_input("Preço", "409€")
cidade = st.text_input("Cidade de partida", "Porto")
datas = st.text_input("Datas", "7 a 15 Março")
hotel = st.text_input("Hotel", "Hotel Herculaneum")
refeicao = st.text_input("Refeição", "Pequeno Almoço")
bagagem = st.text_input("Bagagem", "Bagagem de mão")
transfer = st.text_input("Transfer", "Transfer In + Out")

# --- Imagem de fundo ---
st.markdown("### 🖼️ Imagem de fundo")
col1, col2 = st.columns(2)
with col1:
    imagem_bg_url = st.text_input(
        "URL da imagem (opcional)", 
        "https://www.melhoresdestinos.com.br/wp-content/uploads/2020/12/quanto-custa-viajar-maldivas-capa2019-01.jpg"
    )
with col2:
    upload_bg = st.file_uploader("Ou faz upload da imagem", type=["jpg", "jpeg", "png"])

# --- Fontes ---
try:
    fonte_titulo = ImageFont.truetype("Montserrat-Bold.ttf", 180)
    fonte_subtitulo = ImageFont.truetype("Montserrat-Regular.ttf", 45)
    fonte_info = ImageFont.truetype("Montserrat-SemiBold.ttf", 40)
    fonte_pequena = ImageFont.truetype("Montserrat-Regular.ttf", 28)
except:
    fonte_titulo = ImageFont.load_default()
    fonte_subtitulo = ImageFont.load_default()
    fonte_info = ImageFont.load_default()
    fonte_pequena = ImageFont.load_default()

# Função para centralizar texto
def centralizar_texto(draw, texto, fonte, y, largura, cor=(255, 255, 255)):
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    w = bbox[2] - bbox[0]
    draw.text(((largura - w) / 2, y), texto, fill=cor, font=fonte)

# --- Gerar Card ---
if st.button("🎨 Gerar Card"):
    try:
        # Carregar imagem de fundo (upload ou URL)
        if upload_bg is not None:
            bg_img = Image.open(upload_bg).convert("RGBA")
        else:
            response = requests.get(imagem_bg_url)
            response.raise_for_status()
            bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")

        bg_img = bg_img.resize((largura, altura))
        draw = ImageDraw.Draw(bg_img)

        # --- Overlay preto semitransparente ---
        overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, 60))
        bg_img = Image.alpha_composite(bg_img, overlay)
        draw = ImageDraw.Draw(bg_img)

        # --- Topo fixo ---
        centralizar_texto(draw, "CONSULTOR INDEPENDENTE RNAVT3301", fonte_pequena, 40, largura)
        centralizar_texto(draw, "iCliGo travel consultant", fonte_pequena, 90, largura)

        # --- Subtítulo ---
        centralizar_texto(draw, subtitulo.upper(), fonte_subtitulo, int(altura * 0.25), largura)

        # --- Destino ---
        centralizar_texto(draw, destino.upper(), fonte_titulo, int(altura * 0.33), largura, cor=(0, 255, 174))

        # --- Preço ---
        centralizar_texto(draw, "DESDE", fonte_pequena, int(altura * 0.53), largura)
        centralizar_texto(draw, preco, fonte_titulo.font_variant(size=120), int(altura * 0.57), largura, cor=(0, 255, 174))
        centralizar_texto(draw, "POR PESSOA", fonte_pequena, int(altura * 0.68), largura)

        # --- Ícones e texto ---
        icon_texts = [
            (cidade + "\n" + datas, "✈️"),
            ("HOTEL\n" + hotel, "🏨"),
            (refeicao, "🍽️"),
            (bagagem, "🧳"),
            (transfer, "🚐"),
        ]

        icon_y = int(altura * 0.78)
        spacing = largura // 5

        for i, (texto, icone) in enumerate(icon_texts):
            x = spacing * i + spacing // 2
            bbox = draw.textbbox((0, 0), icone, font=fonte_info)
            w = bbox[2] - bbox[0]
            draw.text((x - w / 2, icon_y), icone, fill=(0, 255, 174), font=fonte_info)
            bbox2 = draw.textbbox((0, 0), texto, font=fonte_pequena)
            w2 = bbox2[2] - bbox2[0]
            draw.multiline_text((x - w2 / 2, icon_y + 70), texto.upper(), fill=(255, 255, 255), font=fonte_pequena, align="center", spacing=5)

        # --- Rodapé ---
        centralizar_texto(draw, "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES.", fonte_pequena, altura - 60, largura)

        # Converter e mostrar
        st.image(bg_img, caption="Pré-visualização", use_container_width=True)

        buf = io.BytesIO()
        bg_img.save(buf, format="PNG")
        st.download_button(
            label="⬇️ Fazer download do card",
            data=buf.getvalue(),
            file_name="card_viagem.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"❌ Erro ao gerar imagem: {e}")

