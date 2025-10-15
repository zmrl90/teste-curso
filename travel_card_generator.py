import streamlit as st
from io import BytesIO
from PIL import Image
import requests

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="Gerador de Card - Viagens", page_icon="🧳", layout="centered")

st.title("🧳 Gerador de Card de Viagem")
st.markdown("---")

st.write("""
**Esta aplicação gera automaticamente cards personalizados de viagens.**  
Escolhe o formato, preenche os campos e faz download da imagem final.
""")

# =========================
# FORMULÁRIO
# =========================
with st.form("card_form"):

    # Escolha do formato
    st.subheader("📐 Formato do Card")
    formato = st.selectbox(
        "Escolhe o tamanho do card:",
        ("1920x1080", "1080x1080", "1440x1080"),
        index=1
    )

    largura, altura = map(int, formato.split("x"))

    st.markdown("---")

    # Campos do card
    st.subheader("🌍 Informações do Destino")
    subtitulo = st.text_input("Frase de Apresentação", value="")
    destino = st.text_input("Destino", value="")
    preco = st.text_input("Preço", value="")
    cidade = st.text_input("Cidade de Partida", value="")
    datas = st.text_input("Datas da Viagem", value="")
    hotel = st.text_input("Hotel", value="")
    regime = st.text_input("Regime Alimentar", value="")
    bagagem = st.text_input("Bagagem", value="")
    transfer = st.text_input("Transfer", value="")
    imagem_bg = st.text_input(
        "URL da Imagem de Fundo",
        value="https://www.melhoresdestinos.com.br/wp-content/uploads/2020/12/quanto-custa-viajar-maldivas-capa2019-01.jpg"
    )

    submit = st.form_submit_button("🎨 Gerar Card", type="primary")

# =========================
# GERAÇÃO DO CARD
# =========================
if submit:
    st.markdown("---")

    consultor = "Consultor Independente RNAVT3301"
    empresa = "iCliGo Travel Consultant"

    # HTML do card
    html_code = f"""
    <div style="position:relative;width:{largura}px;height:{altura}px;
                background-image:url('{imagem_bg}');
                background-size:cover;background-position:center;
                color:white;display:flex;flex-direction:column;
                justify-content:space-between;text-align:center;">
      <div style="position:absolute;inset:0;background:rgba(0,0,0,0.4);"></div>

      <div style="position:relative;padding-top:2rem;">
        <p style="text-transform:uppercase;opacity:0.8;">{consultor}</p>
        <p style="font-weight:300;font-size:1.2rem;">{empresa}</p>
      </div>

      <div style="position:relative;margin-top:3rem;">
        <p style="text-transform:uppercase;letter-spacing:0.2em;margin-bottom:0.5rem;">{subtitulo}</p>
        <h1 style="font-size:5rem;font-weight:700;color:#00ffae;">{destino}</h1>
      </div>

      <div style="position:relative;margin-top:1rem;">
        <p style="text-transform:uppercase;opacity:0.7;">Desde</p>
        <p style="color:#00ffae;font-size:4rem;font-weight:800;">{preco}</p>
        <p style="text-transform:uppercase;">Por pessoa</p>
      </div>

      <div style="position:relative;display:grid;grid-template-columns:repeat(5,1fr);
                  gap:1rem;margin:3rem 0;text-transform:uppercase;font-size:0.9rem;">
        <div>
          <span style="font-size:2rem;color:#00ffae;">✈️</span>
          <p>{cidade}<br>{datas}</p>
        </div>
        <div>
          <span style="font-size:2rem;color:#00ffae;">🏨</span>
          <p>Hotel<br>{hotel}</p>
        </div>
        <div>
          <span style="font-size:2rem;color:#00ffae;">🍽️</span>
          <p>{regime}</p>
        </div>
        <div>
          <span style="font-size:2rem;color:#00ffae;">🧳</span>
          <p>{bagagem}</p>
        </div>
        <div>
          <span style="font-size:2rem;color:#00ffae;">🚐</span>
          <p>{transfer}</p>
        </div>
      </div>

      <div style="position:relative;font-size:0.7rem;opacity:0.7;padding-bottom:2rem;">
        Valor baseado em 2 adultos. Preços sujeitos a alterações.
      </div>
    </div>
    """

    # Mostrar pré-visualização
    st.markdown("### 💻 Pré-visualização do Card:")
    st.components.v1.html(html_code, height=altura + 50)

    # Tentar gerar imagem com PIL
    try:
        bg_img = Image.open(requests.get(imagem_bg, stream=True).raw).convert("RGB")
        bg_img = bg_img.resize((largura, altura))
        buffer = BytesIO()
        bg_img.save(buffer, format="PNG")
        buffer.seek(0)

        st.download_button(
            label="📥 Fazer download da imagem",
            data=buffer,
            file_name=f"card_viagem_{destino or 'destino'}.png",
            mime="image/png"
        )

    except Exception as e:
        st.error("⚠️ Não foi possível gerar a imagem de fundo para download.")
        st.write(e)

    st.markdown("### 📋 Código HTML Gerado:")
    st.code(html_code, language="html")

