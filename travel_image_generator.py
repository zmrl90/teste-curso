# Gerador de Imagens de Viagem
# Aplicação que cria imagens personalizadas baseadas em um template de viagem

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

def create_travel_image(nome_destino, informacao):
    """
    Cria uma imagem de viagem personalizada baseada no template fornecido.
    
    Args:
        nome_destino (str): Nome do destino (ex: "NÁPOLES")
        informacao (str): Informação adicional para mostrar na parte inferior
    
    Returns:
        PIL.Image: Imagem gerada
    """
    
    # Criar uma imagem base (simulando o template)
    # Tamanho similar ao template: 1200x800 pixels
    width, height = 1200, 800
    
    # Criar imagem com fundo azul (simulando o mar)
    image = Image.new('RGB', (width, height), color='#4A90E2')
    
    # Adicionar gradiente para simular o céu
    draw = ImageDraw.Draw(image)
    
    # Criar gradiente do céu
    for y in range(height // 3):
        # Cor vai de azul claro para azul escuro
        color_value = int(255 - (y / (height // 3)) * 100)
        color = (color_value, color_value + 50, 255)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Adicionar "montanhas" no fundo (formas simples)
    mountain_color = (100, 80, 120)  # Roxo escuro
    draw.polygon([(0, height//3), (width//4, height//4), (width//2, height//3)], fill=mountain_color)
    draw.polygon([(width//2, height//3), (3*width//4, height//5), (width, height//3)], fill=mountain_color)
    
    # Adicionar "edifícios" (retângulos coloridos)
    building_colors = ['#FFB366', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    for i in range(5):
        x = 200 + i * 150
        y = height//2
        w = 100
        h = height//3
        draw.rectangle([x, y, x+w, y+h], fill=building_colors[i % len(building_colors)])
    
    # Tentar carregar uma fonte, se não conseguir usar a padrão
    try:
        # Tentar usar uma fonte maior e mais bonita
        title_font = ImageFont.truetype("arial.ttf", 80)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        info_font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Usar fonte padrão se não conseguir carregar arial
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
    
    # Cores para o texto
    green_color = '#00D4AA'  # Verde vibrante como no template
    white_color = '#FFFFFF'
    
    # Adicionar texto do cabeçalho
    header_text = "CONSULTOR INDEPENDENTE RNAVT3301"
    draw.text((width//2 - 200, 20), header_text, fill=white_color, font=subtitle_font)
    
    # Adicionar logo "iCliGo"
    logo_text = "iCliGo"
    draw.text((width//2 - 60, 50), logo_text, fill=green_color, font=subtitle_font)
    
    # Adicionar "travel consultant"
    consultant_text = "travel consultant"
    draw.text((width//2 - 80, 80), consultant_text, fill=white_color, font=info_font)
    
    # Adicionar frase principal
    main_text = "ENTRE O SABOR DA PIZZA E A VISTA DO VESÚVIO - NÁPOLES ENCANTA"
    draw.text((50, 150), main_text, fill=white_color, font=subtitle_font)
    
    # Adicionar NOME DO DESTINO (o mais importante)
    nome_upper = nome_destino.upper()
    # Calcular posição centralizada
    bbox = draw.textbbox((0, 0), nome_upper, font=title_font)
    text_width = bbox[2] - bbox[0]
    x_pos = (width - text_width) // 2
    draw.text((x_pos, 200), nome_upper, fill=green_color, font=title_font)
    
    # Adicionar preço (fixo por enquanto)
    price_text = "409€"
    draw.text((width - 200, height - 150), price_text, fill=green_color, font=title_font)
    draw.text((width - 180, height - 120), "POR PESSOA", fill=white_color, font=info_font)
    draw.text((width - 200, height - 90), "DESDE", fill=white_color, font=info_font)
    
    # Adicionar informações personalizadas na parte inferior
    if informacao:
        # Dividir a informação em linhas se for muito longa
        words = informacao.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 30:  # Limite de caracteres por linha
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Desenhar cada linha
        y_start = height - 60 - (len(lines) * 25)
        for i, line in enumerate(lines):
            draw.text((50, y_start + i * 25), line, fill=white_color, font=info_font)
    
    # Adicionar disclaimer na parte inferior
    disclaimer = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES"
    draw.text((width//2 - 200, height - 30), disclaimer, fill=white_color, font=info_font)
    
    return image

def main():
    """Função principal da aplicação Streamlit"""
    
    # Configurar a página
    st.set_page_config(
        page_title="Gerador de Imagens de Viagem",
        page_icon="✈️",
        layout="wide"
    )
    
    # Título da aplicação
    st.title("✈️ Gerador de Imagens de Viagem")
    st.markdown("---")
    
    # Explicação simples
    st.write("""
    Esta aplicação cria imagens personalizadas para promoções de viagem!
    
    **Como usar:**
    1. Digite o nome do destino (ex: NÁPOLES, ROMA, PARIS)
    2. Adicione informações extras (datas, hotel, etc.)
    3. Clique em "Gerar Imagem" 
    4. Baixe sua imagem personalizada
    """)
    
    # Criar colunas para melhor organização
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Personalizar Imagem")
        
        # Campo para o nome do destino
        nome_destino = st.text_input(
            "Nome do Destino:",
            value="NÁPOLES",
            help="Digite o nome do destino que aparecerá na imagem"
        )
        
        # Campo para informações adicionais
        informacao = st.text_area(
            "Informações Adicionais:",
            value="PORTO 7 A 15 MARÇO | HOTEL HERCULANEUM | PEQUENO ALMOÇO | BAGAGEM DE MÃO | TRANSFER IN+OUT",
            help="Digite as informações que aparecerão na parte inferior da imagem",
            height=100
        )
        
        # Botão para gerar imagem
        if st.button("🎨 Gerar Imagem", type="primary"):
            if nome_destino:
                # Mostrar loading
                with st.spinner("Gerando sua imagem..."):
                    # Criar a imagem
                    image = create_travel_image(nome_destino, informacao)
                    
                    # Salvar no estado da sessão
                    st.session_state.generated_image = image
                    st.success("Imagem gerada com sucesso!")
            else:
                st.error("Por favor, digite o nome do destino!")
    
    with col2:
        st.subheader("🖼️ Imagem Gerada")
        
        # Mostrar a imagem se foi gerada
        if 'generated_image' in st.session_state:
            # Converter para RGB se necessário
            image = st.session_state.generated_image.convert('RGB')
            
            # Mostrar a imagem
            st.image(image, caption="Sua imagem personalizada", use_column_width=True)
            
            # Botão para download
            # Converter imagem para bytes
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            st.download_button(
                label="📥 Baixar Imagem",
                data=img_buffer.getvalue(),
                file_name=f"viagem_{nome_destino.lower().replace(' ', '_')}.png",
                mime="image/png"
            )
        else:
            st.info("👆 Preencha os campos à esquerda e clique em 'Gerar Imagem' para ver sua imagem aqui!")
    
    # Rodapé
    st.markdown("---")
    st.caption("💡 Dica: Use letras maiúsculas para o nome do destino para melhor resultado!")

if __name__ == "__main__":
    main()
