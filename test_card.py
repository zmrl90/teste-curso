from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def create_simple_card():
    # Criar imagem
    width, height = 1080, 1350
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Carregar imagem de fundo
    try:
        response = requests.get("https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1400&auto=format&fit=crop", timeout=10)
        bg_img = Image.open(BytesIO(response.content))
        bg_img = bg_img.resize((width, height))
        img.paste(bg_img, (0, 0))
        draw = ImageDraw.Draw(img)
    except:
        pass
    
    # Overlay escuro
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Cores
    white = (255, 255, 255)
    green = (0, 255, 174)
    
    # Tentar usar fonte do sistema
    try:
        font_huge = ImageFont.truetype("arial.ttf", 300)  # MUITO GRANDE!
        font_price = ImageFont.truetype("arial.ttf", 200)  # MUITO GRANDE!
        font_medium = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_huge = ImageFont.load_default()
        font_price = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Textos
    # Consultor (topo)
    draw.text((width//2, 50), "CONSULTOR INDEPENDENTE RNAVT3301", font=font_small, fill=white, anchor="mt")
    draw.text((width//2, 100), "iCliGo travel consultant", font=font_small, fill=white, anchor="mt")
    
    # Subtítulo
    draw.text((width//2, 200), "ENTRE O SABOR DA PIZZA E A VISTA DO VESÚVIO", font=font_medium, fill=white, anchor="mt")
    
    # DESTINO - ENORME!
    dest_text = "NÁPOLES"
    dest_bbox = draw.textbbox((0, 0), dest_text, font=font_huge)
    dest_width = dest_bbox[2] - dest_bbox[0]
    dest_x = (width - dest_width) // 2
    draw.text((dest_x, 400), dest_text, font=font_huge, fill=green)
    
    # Preço - ENORME!
    price_text = "409€"
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_width = price_bbox[2] - price_bbox[0]
    price_x = int(width * 0.75) - price_width // 2
    
    draw.text((price_x, 800), "DESDE", font=font_medium, fill=white, anchor="mt")
    draw.text((price_x, 850), price_text, font=font_price, fill=green, anchor="mt")
    draw.text((price_x, 1080), "POR PESSOA", font=font_medium, fill=white, anchor="mt")
    
    # Ícones
    icons_y = 1200
    icon_data = ["✈ PORTO", "🏨 HOTEL", "🍽 PEQUENO ALMOÇO", "💼 BAGAGEM", "🚐 TRANSFER"]
    spacing = width // len(icon_data)
    
    for i, icon_text in enumerate(icon_data):
        x = spacing * i + spacing // 2
        draw.text((x, icons_y), icon_text, font=font_small, fill=white, anchor="mt")
    
    return img

if __name__ == "__main__":
    print("A criar card de teste...")
    card = create_simple_card()
    card.save("teste_card.png")
    print("Card criado: teste_card.png")
    print("Abrindo imagem...")
    card.show()
