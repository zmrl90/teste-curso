import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

st.set_page_config(page_title="Gerador de Card de Viagem - Simples", layout="centered")

# Função para baixar fontes
def get_font(size):
    try:
        # Tenta usar uma fonte do sistema primeiro
        return ImageFont.truetype("arial.ttf", size)
    except:
        try:
            # Tenta outras fontes do sistema
            return ImageFont.truetype("calibri.ttf", size)
        except:
            try:
                return ImageFont.truetype("verdana.ttf", size)
            except:
                # Fallback para fonte padrão
                return ImageFont.load_default()

# Função para criar o card
def create_travel_card(destination, price, subtitle, image_url, width=1080, height=1350):
    # Criar imagem base
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Carregar imagem de fundo se fornecida
    if image_url:
        try:
            response = requests.get(image_url, timeout=10)
            bg_img = Image.open(BytesIO(response.content))
            bg_img = bg_img.resize((width, height))
            img.paste(bg_img, (0, 0))
            draw = ImageDraw.Draw(img)
        except:
            pass
    
    # Adicionar overlay escuro
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Cores
    white = (255, 255, 255)
    green = (0, 255, 174)
    
    # Texto do consultor (topo)
    font_small = get_font(30)
    # Calcular posição centralizada manualmente
    text1 = "CONSULTOR INDEPENDENTE RNAVT3301"
    bbox1 = draw.textbbox((0, 0), text1, font=font_small)
    text1_width = bbox1[2] - bbox1[0]
    draw.text(((width - text1_width) // 2, 50), text1, font=font_small, fill=white)
    
    text2 = "iCliGo travel consultant"
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    text2_width = bbox2[2] - bbox2[0]
    draw.text(((width - text2_width) // 2, 90), text2, font=font_small, fill=white)
    
    # Subtítulo
    font_medium = get_font(40)
    bbox_sub = draw.textbbox((0, 0), subtitle.upper(), font=font_medium)
    sub_width = bbox_sub[2] - bbox_sub[0]
    draw.text(((width - sub_width) // 2, 200), subtitle.upper(), font=font_medium, fill=white)
    
    # DESTINO - MUITO GRANDE
    font_huge = get_font(300)  # AINDA MAIS GRANDE!
    dest_text = destination.upper()
    dest_bbox = draw.textbbox((0, 0), dest_text, font=font_huge)
    dest_width = dest_bbox[2] - dest_bbox[0]
    dest_x = (width - dest_width) // 2
    draw.text((dest_x, 400), dest_text, font=font_huge, fill=green)
    
    # Preço - MUITO GRANDE
    font_price = get_font(200)  # AINDA MAIS GRANDE!
    price_text = price
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_width = price_bbox[2] - price_bbox[0]
    price_x = int(width * 0.75) - price_width // 2
    
    # "DESDE"
    desde_bbox = draw.textbbox((0, 0), "DESDE", font=font_medium)
    desde_width = desde_bbox[2] - desde_bbox[0]
    draw.text((price_x - desde_width//2, 800), "DESDE", font=font_medium, fill=white)
    
    # Preço
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_width = price_bbox[2] - price_bbox[0]
    draw.text((price_x - price_width//2, 850), price_text, font=font_price, fill=green)
    
    # "POR PESSOA"
    pessoa_bbox = draw.textbbox((0, 0), "POR PESSOA", font=font_medium)
    pessoa_width = pessoa_bbox[2] - pessoa_bbox[0]
    draw.text((price_x - pessoa_width//2, 1020), "POR PESSOA", font=font_medium, fill=white)
    
    # Ícones e detalhes (parte inferior)
    icons_y = 1100
    font_icon = get_font(35)
    
    # Ícones simples
    icon_data = [
        ("✈", "PORTO\n7 A 15 MARÇO"),
        ("🏨", "HOTEL\nHERCULANEUM"),
        ("🍽", "PEQUENO\nALMOÇO"),
        ("💼", "BAGAGEM\nDE MÃO"),
        ("🚐", "TRANSFER\nIN+OUT")
    ]
    
    spacing = width // len(icon_data)
    for i, (icon, text) in enumerate(icon_data):
        x = spacing * i + spacing // 2
        # Ícone
        icon_bbox = draw.textbbox((0, 0), icon, font=get_font(60))
        icon_width = icon_bbox[2] - icon_bbox[0]
        draw.text((x - icon_width//2, icons_y - 50), icon, font=get_font(60), fill=green)
        
        # Texto
        text_bbox = draw.textbbox((0, 0), text, font=font_icon)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((x - text_width//2, icons_y), text, font=font_icon, fill=white)
    
    # Rodapé
    footer_font = get_font(25)
    footer_text = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES."
    footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, height - 50), footer_text, font=footer_font, fill=white)
    
    return img

# Interface Streamlit
st.title("🧳 Gerador de Card de Viagem - Versão Simples")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Conteúdo")
    destination = st.text_input("Destino", "NÁPOLES")
    price = st.text_input("Preço", "409€")
    subtitle = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta")

with col2:
    st.subheader("Configurações")
    image_url = st.text_input("URL da imagem de fundo", 
                             "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1400&auto=format&fit=crop")
    
    width = st.selectbox("Largura", [1080, 1920], index=0)
    height = st.selectbox("Altura", [1350, 1080, 1920], index=0)

if st.button("🎨 Gerar Card"):
    with st.spinner("A gerar card..."):
        try:
            card = create_travel_card(destination, price, subtitle, image_url, width, height)
            
            st.markdown("### Pré-visualização")
            st.image(card, use_column_width=True)
            
            # Download
            buf = BytesIO()
            card.save(buf, format="PNG")
            buf.seek(0)
            st.download_button("⬇️ Fazer download", data=buf, file_name="card_viagem.png", mime="image/png")
            
        except Exception as e:
            st.error(f"Erro: {e}")
