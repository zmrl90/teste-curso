import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# -------- FUNÇÃO PARA CARREGAR A FONTE --------
def load_font(size):
    return ImageFont.truetype("Montserrat-Regular.ttf", size)

# -------- FUNÇÃO PRINCIPAL --------
def criar_card(fundo: Image.Image,
               titulo: str,
               destino: str,
               preco: str,
               extras: list,
               formato: str):
    if formato == "Feed (1080x1080)":
        W, H = 1080, 1080
    else:
        W, H = 1080, 1920

    # Ajustar imagem de fundo (cover)
    fundo = fundo.copy()
    fundo_ratio = fundo.width / fundo.height
    target_ratio = W / H

    if fundo_ratio > target_ratio:
        new_width = int(fundo.height * target_ratio)
        offset = (fundo.width - new_width) // 2
        fundo = fundo.crop((offset, 0, offset + new_width, fundo.height))
    else:
        new_height = int(fundo.width / target_ratio)
        offset = (fundo.height - new_height) // 2
        fundo = fundo.crop((0, offset, fundo.width, offset + new_height))

    fundo = fundo.resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(fundo)

    # -------- CORES E FONTES --------
    cor_texto = (0, 255, 179)  # verde neon
    cor_sombra = (0, 0, 0, 200)
    font_titulo = load_font(80 if formato.startswith("Feed") else 120)
    font_destino = load_font(45 if formato.startswith("Feed") else 70)
    font_preco = load_font(220 if formato.startswith("Feed") else 300)
    font_extra = load_font(36 if formato.startswith("Feed") else 54)

    # -------- POSIÇÕES (baseadas no template) --------
    # Título – topo esquerdo
    pos_titulo = (80, 80)
    draw.text((pos_titulo[0]+3, pos_titulo[1]+3), titulo, font=font_titulo, fill=cor_sombra)
    draw.text(pos_titulo, titulo, font=font_titulo, fill=cor_texto)

    # Destino – logo abaixo do título
    w_t, h_t = draw.textsize(titulo, font=font_titulo)
    pos_destino = (80, pos_titulo[1] + h_t + 15)
    draw.text((pos_destino[0]+2, pos_destino[1]+2), destino, font=font_destino, fill=cor_sombra)
    draw.text(pos_destino, destino, font=font_destino, fill=cor_texto)

    # Preço – grande, à direita e centrado verticalmente
    w_p, h_p = draw.textsize(preco, font=font_preco)
    x_prec = W - w_p - 100  # 100 px da margem direita
    y_prec = (H // 2) - (h_p // 2) - 50
    draw.text((x_prec+4, y_prec+4), preco, font=font_preco, fill=cor_sombra)
    draw.text((x_prec, y_prec), preco, font=font_preco, fill=cor_texto)

    # Extras – linha única em baixo, centrada
    extras_text = "   •   ".join(extras)
    w_e, h_e = draw.textsize(extras_text, font=font_extra)
    x_extras = (W - w_e) // 2
    y_extras = H - h_e - 80
    draw.text((x_extras+2, y_extras+2), extras_text, font=font_extra, fill=cor_sombra)
    draw.text((x_extras, y_extras), extras_text, font=font_extra, fill=cor_texto)

    return fundo

# -------- INTERFACE STREAMLIT --------
st.set_page_config(page_title="Gerador de Card de Viagem", layout="centered")

st.title("🌴 Gerador de Card de Viagem")

f_upload = st.file_uploader("📸 Escolhe a imagem de fundo", type=["jpg","jpeg","png"])
if f_upload:
    img = Image.open(f_upload).convert("RGB")

    st.markdown("### ✍️ Informações do Card")
    titulo = st.text_input("Título principal", "CONSULTOR INDEPENDENTE RNAVT 3301")
    destino = st.text_input("Destino / Subtítulo", "Nápoles encanta")
    preco = st.text_input("Preço", "409 €")
    extras = st.text_area("Extras (1 por linha)", "Hotel Herculaneum\nPequeno-almoço\nTransfer in + out")
    lista_extras = [x.strip() for x in extras.split("\n") if x.strip()]

    formato = st.radio("Formato do card", ["Feed (1080x1080)", "Story (1080x1920)"])

    if st.button("🚀 Gerar Card"):
        card = criar_card(img, titulo, destino, preco, lista_extras, formato)
        st.image(card, use_container_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="💾 Download da Imagem",
            data=byte_im,
            file_name=f"card_viagem_{formato.replace(' ','_')}.png",
            mime="image/png"
        )



