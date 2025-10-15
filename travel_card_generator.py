import streamlit as st
from PIL import Image

# === CONFIGURAÇÕES GERAIS ===
st.set_page_config(layout="centered")

# === FONTE MONTSERRAT ===
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            font-family: 'Montserrat', sans-serif;
        }
        body {
            background-color: #000;
        }
        .overlay {
            position: relative;
            text-align: center;
            color: white;
        }
        .overlay img {
            width: 100%;
            opacity: 0.85;
        }
        .centered-text {
            position: absolute;
            top: 10%;
            left: 50%;
            transform: translate(-50%, 0%);
            width: 100%;
        }
        h1 {
            font-size: 90px;
            font-weight: 700;
            color: #00FFC6;
            margin: 10px 0;
        }
        .small-text {
            font-size: 14px;
        }
        .price {
            font-size: 60px;
            color: #00FFC6;
            font-weight: 700;
        }
        .icons {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-top: 550px;
            color: white;
            font-size: 14px;
        }
        .icons div {
            text-align: center;
        }
        .footer {
            text-align: center;
            color: white;
            font-size: 10px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# === UPLOAD DA IMAGEM ===
uploaded_image = st.file_uploader("📸 Carrega a imagem de fundo", type=["jpg", "png"])

if uploaded_image:
    st.markdown("<div class='overlay'>", unsafe_allow_html=True)
    st.image(uploaded_image, use_column_width=True)
    st.markdown("""
        <div class='centered-text'>
            <p style='font-size: 12px;'>CONSULTOR INDEPENDENTE RNAVT3301</p>
            <p style='font-size: 16px; font-weight: 600;'>iCliGo travel consultant</p>
            <p class='small-text' style='margin-top: 40px;'>ENTRE O SABOR DA PIZZA E A VISTA DO VESÚVIO — NÁPOLES ENCANTA</p>
            <h1>NÁPOLES</h1>
            <p class='small-text'>DESDE</p>
            <p class='price'>409€</p>
            <p class='small-text'>POR PESSOA</p>
        </div>

        <div class='icons'>
            <div>✈️<br>PORTO<br>7 A 15 MARÇO</div>
            <div>🏨<br>HOTEL<br>HERCULANEUM</div>
            <div>🍽️<br>PEQUENO<br>ALMOÇO</div>
            <div>🧳<br>BAGAGEM<br>DE MÃO</div>
            <div>🚐<br>TRANSFER<br>IN+OUT</div>
        </div>

        <p class='footer'>VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES.</p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("⬆️ Carrega uma imagem de fundo para ver o cartão completo.")
