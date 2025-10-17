import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

st.set_page_config(page_title="Gerador de Card de Viagem - Completo", layout="centered")

# Função para obter fontes
def get_font(size, bold=False):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        try:
            return ImageFont.truetype("calibri.ttf", size)
        except:
            try:
                return ImageFont.truetype("verdana.ttf", size)
            except:
                return ImageFont.load_default()

# Função para centralizar texto
def center_text(draw, text, font, x_center, y, fill=(255, 255, 255)):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text((x_center - text_width//2, y), text, font=font, fill=fill)

# Função principal para criar o card
def create_travel_card(data, width=1080, height=1350):
    # Criar imagem base
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Carregar imagem de fundo
    if data['image_mode'] == 'upload_local' and data['upload_image']:
        try:
            bg_img = Image.open(data['upload_image'])
            bg_img = bg_img.resize((width, height))
            img.paste(bg_img, (0, 0))
            draw = ImageDraw.Draw(img)
        except Exception as e:
            st.warning(f"Erro ao carregar imagem: {e}")
    elif data['image_mode'] == 'url_da_web' and data['image_url']:
        try:
            response = requests.get(data['image_url'], timeout=10)
            bg_img = Image.open(BytesIO(response.content))
            bg_img = bg_img.resize((width, height))
            img.paste(bg_img, (0, 0))
            draw = ImageDraw.Draw(img)
        except Exception as e:
            st.warning(f"Erro ao carregar imagem da URL: {e}")
    
    # Adicionar overlay escuro
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 90))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Cores
    white = (255, 255, 255)
    accent_rgb = tuple(int(data['accent_color'].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    
    # Fontes
    font_consultor = get_font(30)
    font_subtitle = get_font(40)
    font_destination = get_font(300, bold=True)  # ENORME!
    font_price_label = get_font(50)
    font_price = get_font(200, bold=True)  # ENORME!
    font_price_by = get_font(45)
    font_icon = get_font(35)
    font_icon_emoji = get_font(60)
    font_footer = get_font(25)
    
    # 1. Texto do consultor (topo)
    center_text(draw, data['consultor_line1'].upper(), font_consultor, width//2, 50, white)
    center_text(draw, data['consultor_line2'], font_consultor, width//2, 90, white)
    
    # 2. Subtítulo
    center_text(draw, data['subtitle'].upper(), font_subtitle, width//2, 200, white)
    
    # 3. DESTINO - MUITO GRANDE
    dest_text = data['destination'].upper()
    center_text(draw, dest_text, font_destination, width//2, 400, accent_rgb)
    
    # 4. Preço (lado direito)
    price_x = int(width * 0.75)
    
    # "DESDE"
    center_text(draw, data['price_label'].upper(), font_price_label, price_x, 800, white)
    
    # Preço principal
    center_text(draw, data['price'], font_price, price_x, 850, accent_rgb)
    
    # "POR PESSOA"
    center_text(draw, data['price_by'].upper(), font_price_by, price_x, 1020, white)
    
    # 5. Ícones e detalhes (parte inferior)
    icons_y = 1100
    icon_data = [
        (data['icon1_emoji'], data['icon1_text']),
        (data['icon2_emoji'], data['icon2_text']),
        (data['icon3_emoji'], data['icon3_text']),
        (data['icon4_emoji'], data['icon4_text']),
        (data['icon5_emoji'], data['icon5_text'])
    ]
    
    spacing = width // len(icon_data)
    for i, (emoji, text) in enumerate(icon_data):
        x = spacing * i + spacing // 2
        
        # Ícone emoji
        center_text(draw, emoji, font_icon_emoji, x, icons_y - 50, accent_rgb)
        
        # Texto do ícone
        center_text(draw, text.upper(), font_icon, x, icons_y, white)
    
    # 6. Rodapé
    center_text(draw, data['footer'].upper(), font_footer, width//2, height - 50, white)
    
    return img

# Interface Streamlit
st.title("🧳 Gerador de Card de Viagem - Completo")
st.markdown("### Crie cartões de viagem personalizados como no template!")

with st.form("card_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Conteúdo do Card")
        
        # Consultor
        st.markdown("**Informações do Consultor:**")
        consultor_line1 = st.text_input("Linha 1", "CONSULTOR INDEPENDENTE RNAVT3301")
        consultor_line2 = st.text_input("Linha 2", "iCliGo travel consultant")
        
        # Destino e preço
        st.markdown("**Destino e Preço:**")
        destination = st.text_input("Destino", "NÁPOLES")
        subtitle = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta")
        
        col_price1, col_price2, col_price3 = st.columns(3)
        with col_price1:
            price_label = st.text_input("Rótulo do preço", "DESDE")
        with col_price2:
            price = st.text_input("Preço", "409€")
        with col_price3:
            price_by = st.text_input("Texto abaixo do preço", "POR PESSOA")
        
        # Ícones e detalhes
        st.markdown("**Detalhes da Viagem (Ícones):**")
        col_icon1, col_icon2, col_icon3, col_icon4, col_icon5 = st.columns(5)
        
        with col_icon1:
            icon1_emoji = st.text_input("Ícone 1", "✈", key="icon1")
            icon1_text = st.text_input("Texto 1", "PORTO\n7 A 15 MARÇO", key="text1")
        
        with col_icon2:
            icon2_emoji = st.text_input("Ícone 2", "🏨", key="icon2")
            icon2_text = st.text_input("Texto 2", "HOTEL\nHERCULANEUM", key="text2")
        
        with col_icon3:
            icon3_emoji = st.text_input("Ícone 3", "🍽", key="icon3")
            icon3_text = st.text_input("Texto 3", "PEQUENO\nALMOÇO", key="text3")
        
        with col_icon4:
            icon4_emoji = st.text_input("Ícone 4", "💼", key="icon4")
            icon4_text = st.text_input("Texto 4", "BAGAGEM\nDE MÃO", key="text4")
        
        with col_icon5:
            icon5_emoji = st.text_input("Ícone 5", "🚐", key="icon5")
            icon5_text = st.text_input("Texto 5", "TRANSFER\nIN+OUT", key="text5")
        
        # Rodapé
        footer = st.text_input("Rodapé", "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES.")
    
    with col2:
        st.subheader("🎨 Configurações")
        
        # Modo de imagem
        image_mode = st.radio("Fonte da imagem de fundo", ["Upload local", "URL da web"], index=0)
        
        if image_mode == "Upload local":
            upload_image = st.file_uploader("Carregar imagem", type=["jpg", "jpeg", "png"], key="upload")
            image_url = ""
        else:
            upload_image = None
            image_url = st.text_input("URL da imagem", 
                                    "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1400&auto=format&fit=crop",
                                    key="url")
        
        # Formato
        st.markdown("**Formato da imagem:**")
        format_choice = st.selectbox("Tamanho", ["Feed 1080×1350", "Quadrado 1080×1080", "Wide 1920×1080", "Story 1080×1920"], index=0)
        
        # Cores
        accent_color = st.color_picker("Cor de destaque", "#00ffae")
        
        # Nome do ficheiro
        filename = st.text_input("Nome do ficheiro", "card_viagem.png")
    
    # Botão de gerar
    submitted = st.form_submit_button("🎨 Gerar Card de Viagem", use_container_width=True)

# Processar quando o formulário for submetido
if submitted:
    # Determinar tamanhos baseado no formato
    if format_choice == "Feed 1080×1350":
        width, height = 1080, 1350
    elif format_choice == "Quadrado 1080×1080":
        width, height = 1080, 1080
    elif format_choice == "Wide 1920×1080":
        width, height = 1920, 1080
    else:  # Story
        width, height = 1080, 1920
    
    # Preparar dados
    data = {
        'consultor_line1': consultor_line1,
        'consultor_line2': consultor_line2,
        'destination': destination,
        'subtitle': subtitle,
        'price_label': price_label,
        'price': price,
        'price_by': price_by,
        'icon1_emoji': icon1_emoji,
        'icon1_text': icon1_text,
        'icon2_emoji': icon2_emoji,
        'icon2_text': icon2_text,
        'icon3_emoji': icon3_emoji,
        'icon3_text': icon3_text,
        'icon4_emoji': icon4_emoji,
        'icon4_text': icon4_text,
        'icon5_emoji': icon5_emoji,
        'icon5_text': icon5_text,
        'footer': footer,
        'image_mode': image_mode.lower().replace(" ", "_"),
        'upload_image': upload_image,
        'image_url': image_url,
        'accent_color': accent_color
    }
    
    # Gerar card
    with st.spinner("A gerar o seu card de viagem..."):
        try:
            card = create_travel_card(data, width, height)
            
            st.markdown("### ✨ Pré-visualização")
            st.image(card, use_container_width=True)
            
            # Download
            buf = BytesIO()
            card.save(buf, format="PNG")
            buf.seek(0)
            
            st.download_button(
                "⬇️ Fazer Download do Card",
                data=buf,
                file_name=filename,
                mime="image/png",
                use_container_width=True
            )
            
            st.success("🎉 Card gerado com sucesso!")
            
        except Exception as e:
            st.error(f"❌ Erro ao gerar o card: {e}")
            st.exception(e)
