import streamlit as st

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            font-family: 'Montserrat', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)


import streamlit as st
from PIL import Image

st.set_page_config(layout="centered")

# === Upload da imagem de fundo ===
uploaded_image = st.file_uploader("📸 Carrega a imagem de fundo", type=["jpg", "png"])
if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, use_column_width=True)

# === Título e subtítulo ===
st.markdown("""
<div style='text-align: center; color: white; margin-top: -420px;'>
    <p style='font-size: 12px;'>CONSULTOR INDEPENDENTE RNAVT3301</p>
    <p style='font-size: 16px; font-weight: 600;'>iCliGo travel consultant</p>
    <p style='font-size: 14px; margin-top: 40px;'>ENTRE O SABOR DA PIZZA E A VISTA DO VESÚVIO — NÁPOLES ENCANTA</p>
    <h1 style='font-size: 90px; font-weight: 700; margin: 10px 0;'>NÁPOLES</h1>
    <p style='font-size: 14px; margin-top: 10px;'>DESDE</p>
    <p style='font-size: 60px; font-weight: 700; color: #00FFC6;'>409€</p>
    <p style='font-size: 12px;'>POR PESSOA</p>
</div>
""", unsafe_allow_html=True)

# === Linha de ícones ===
st.markdown("""
<div style='display: flex; justify-content: space-around; align-items: center; text-align: center; margin-top: 50px; color: white;'>
    <div><p>✈️<br>PORTO<br>7 A 15 MARÇO</p></div>
    <div><p>🏨<br>HOTEL<br>HERCULANEUM</p></div>
    <div><p>🍽️<br>PEQUENO<br>ALMOÇO</p></div>
    <div><p>🧳<br>BAGAGEM<br>DE MÃO</p></div>
    <div><p>🚐<br>TRANSFER<br>IN+OUT</p></div>
</div>
<p style='text-align: center; color: white; font-size: 10px; margin-top: 20px;'>VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES.</p>
""", unsafe_allow_html=True)
