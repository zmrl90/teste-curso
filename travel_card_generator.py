import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# --------------------
# Helpers
# --------------------
FONT_URLS = {
    "regular": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Regular.ttf",
    "semibold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-SemiBold.ttf",
    "bold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf",
}

def download_font(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return BytesIO(r.content)
    except Exception:
        return None

def load_fonts(default_sizes=(48,40,120)):
    f_reg = download_font(FONT_URLS["regular"])
    f_sem = download_font(FONT_URLS["semibold"])
    f_bold = download_font(FONT_URLS["bold"])
    fonts = {}
    try:
        fonts["reg"] = ImageFont.truetype(f_reg if f_reg else BytesIO(), size=default_sizes[0])
    except Exception:
        fonts["reg"] = ImageFont.load_default()
    try:
        fonts["sem"] = ImageFont.truetype(f_sem if f_sem else BytesIO(), size=default_sizes[1])
    except Exception:
        fonts["sem"] = ImageFont.load_default()
    try:
        fonts["bold"] = ImageFont.truetype(f_bold if f_bold else BytesIO(), size=default_sizes[2])
    except Exception:
        fonts["bold"] = ImageFont.load_default()
    return fonts

def text_size(draw, text, font):
    bbox = draw.textbbox((0,0), text, font=font, stroke_width=0)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]

def draw_centered(draw, text, font, x_center, y, fill=(255,255,255), align="center", stroke_width=2, stroke_fill=(0,0,0)):
    if "\n" in text or isinstance(text, list):
        if isinstance(text, list):
            text = "\n".join(text)
        lines = text.split("\n")
        widths = [text_size(draw, line, font)[0] for line in lines]
        max_w = max(widths) if widths else 0
        start_x = x_center - max_w/2
        draw.multiline_text((start_x, y), text, font=font, fill=fill, align=align, spacing=6,
                            stroke_width=stroke_width, stroke_fill=stroke_fill)
        h_total = sum(text_size(draw, line, font)[1] for line in lines) + (len(lines)-1)*6
        return max_w, h_total
    else:
        w,h = text_size(draw, text, font)
        draw.text((x_center - w/2, y), text, font=font, fill=fill,
                  stroke_width=stroke_width, stroke_fill=stroke_fill)
        return w,h

# --------------------
# Presets por formato (tamanhos/posições “pixel perfect”)
# --------------------
PRESETS = {
    # 1080 × 1350
    "Feed 1080×1350": {
        "size": (1080, 1350),
        "font_sizes": {
            "top_small": 28,       # linhas de topo
            "subtitle": 40,        # linha acima do destino
            "destination": 200,    # DESTINO (pedido)
            "price": 280,          # preço grande
            "price_label": 48,     # "DESDE"
            "price_by": 40,        # "POR PESSOA"
            "icons": 40,           # texto de ícones
            "icons_emoji": 56,     # emoji acima
            "footer": 26           # rodapé
        },
        "positions": {
            "top_y": 36,
            "subtitle_y": 260,
            "destination_y": 380,
            "price_center_x": int(1080*0.74),
            "price_block_top_y": 720,  # y do rótulo "DESDE"
            "icons_y": 1020,
            "footer_y": 1280
        }
    },
    # 1080 × 1080
    "Quadrado 1080×1080": {
        "size": (1080, 1080),
        "font_sizes": {
            "top_small": 26,
            "subtitle": 36,
            "destination": 200,
            "price": 260,
            "price_label": 44,
            "price_by": 36,
            "icons": 36,
            "icons_emoji": 52,
            "footer": 24
        },
        "positions": {
            "top_y": 30,
            "subtitle_y": 220,
            "destination_y": 320,
            "price_center_x": int(1080*0.74),
            "price_block_top_y": 610,
            "icons_y": 840,
            "footer_y": 1000
        }
    },
    # 1920 × 1080 (wide)
    "Wide 1920×1080": {
        "size": (1920, 1080),
        "font_sizes": {
            "top_small": 30,
            "subtitle": 44,
            "destination": 200,
            "price": 280,
            "price_label": 50,
            "price_by": 42,
            "icons": 40,
            "icons_emoji": 60,
            "footer": 26
        },
        "positions": {
            "top_y": 30,
            "subtitle_y": 220,
            "destination_y": 320,
            "price_center_x": int(1920*0.76),
            "price_block_top_y": 560,
            "icons_y": 860,
            "footer_y": 1000
        }
    },
    # 1080 × 1920 (story)
    "Story 1080×1920": {
        "size": (1080, 1920),
        "font_sizes": {
            "top_small": 34,
            "subtitle": 56,
            "destination": 240,     # maior no story
            "price": 320,
            "price_label": 56,
            "price_by": 48,
            "icons": 44,
            "icons_emoji": 64,
            "footer": 28
        },
        "positions": {
            "top_y": 40,
            "subtitle_y": 360,
            "destination_y": 520,
            "price_center_x": int(1080*0.74),
            "price_block_top_y": 980,
            "icons_y": 1460,
            "footer_y": 1820
        }
    }
}

# --------------------
# UI
# --------------------
st.title("🧳 Gerador de Card de Viagem (template: NÁPOLES)")

with st.form("inputs"):
    col_a, col_b = st.columns([2,1])

    with col_a:
        st.subheader("Conteúdo do Card")
        subtitle = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio — Nápoles encanta")
        destination = st.text_input("Destino (grande)", "NÁPOLES")
        price = st.text_input("Preço", "409€")
        price_label = st.text_input("Preço - rótulo acima (ex: Desde)", "DESDE")
        price_by = st.text_input("Texto abaixo do preço", "POR PESSOA")

        st.write("---")
        st.write("Detalhes (linha de ícones)")
        origin = st.text_input("Cidade de Partida", "PORTO")
        dates = st.text_input("Datas", "7 A 15 MARÇO")
        hotel = st.text_input("Hotel", "HOTEL HERCULANEUM")
        meal = st.text_input("Regime", "PEQUENO ALMOÇO")
        baggage = st.text_input("Bagagem", "BAGAGEM DE MÃO")
        transfer = st.text_input("Transfer", "TRANSFER IN + OUT")

    with col_b:
        st.subheader("Imagem e formato")
        input_mode = st.radio("Fonte da imagem de fundo", ("Upload local", "URL"), index=0)
        if input_mode == "Upload local":
            upload = st.file_uploader("Carrega uma imagem (jpg/png)", type=["jpg", "jpeg", "png"])
            image_url = ""
        else:
            upload = None
            image_url = st.text_input("URL da imagem", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1400&auto=format&fit=crop")

        st.write("---")
        fmt = st.selectbox("Formato da imagem", tuple(PRESETS.keys()), index=0)
        outfile_name = st.text_input("Nome do ficheiro para download", "card_viagem.png")
        color_accent = st.color_picker("Cor de destaque (texto & ícones)", "#00ffae")

    submit = st.form_submit_button("🎨 Gerar e Pré-visualizar")

from PIL import ExifTags

# --------------------
# Process & Render (versão corrigida)
# --------------------
if submit:
    preset = PRESETS[fmt]
    (W, H) = preset["size"]
    F = preset["font_sizes"]
    P = preset["positions"]

    # --- carregar imagem com orientação EXIF corrigida ---
    try:
        if upload is not None:
            bg = Image.open(upload)
        else:
            resp = requests.get(image_url, timeout=15); resp.raise_for_status()
            bg = Image.open(BytesIO(resp.content))

        # corrigir orientação EXIF
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(bg._getexif().items())
            if exif[orientation] == 3:
                bg = bg.rotate(180, expand=True)
            elif exif[orientation] == 6:
                bg = bg.rotate(270, expand=True)
            elif exif[orientation] == 8:
                bg = bg.rotate(90, expand=True)
        except Exception:
            pass

        bg = bg.convert("RGBA")
    except Exception as e:
        st.error(f"Erro ao carregar imagem de fundo: {e}")
        st.stop()

    # --- redimensionar e recortar (cover) ---
    bg_ratio = bg.width / bg.height
    target_ratio = W / H
    if bg_ratio > target_ratio:
        new_h = H; new_w = int(bg_ratio * new_h)
    else:
        new_w = W; new_h = int(new_w / bg_ratio)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2; top = (new_h - H) // 2
    bg = bg.crop((left, top, left + W, top + H))

    # --- overlay ligeiro ---
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 100))
    canvas = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(canvas)

    # --- tamanhos absolutos de fonte (não dependem do Streamlit scale) ---
    def load_font_fixed(url, size):
        return ImageFont.truetype(BytesIO(requests.get(url, timeout=15).content), size=size)

    f_top  = load_font_fixed(FONT_URLS["regular"], F["top_small"])
    f_sub  = load_font_fixed(FONT_URLS["regular"], F["subtitle"])
    f_dest = load_font_fixed(FONT_URLS["bold"],    F["destination"])
    f_price= load_font_fixed(FONT_URLS["bold"],    F["price"])
    f_plab = load_font_fixed(FONT_URLS["semibold"],F["price_label"])
    f_pby  = load_font_fixed(FONT_URLS["regular"], F["price_by"])
    f_ic   = load_font_fixed(FONT_URLS["regular"], F["icons"])
    f_icm  = load_font_fixed(FONT_URLS["semibold"],F["icons_emoji"])
    f_foot = load_font_fixed(FONT_URLS["regular"], F["footer"])

    accent_rgb = tuple(int(color_accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # --- topo fixo ---
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", f_top, W//2, P["top_y"], fill=(255,255,255))
    draw_centered(draw, "iCliGo travel consultant", f_top, W//2, P["top_y"] + int(F["top_small"]*1.6), fill=(255,255,255))

    # --- subtítulo ---
    subtitle_wrapped = "\n".join(textwrap.wrap(subtitle.upper(), width=40))
    draw_centered(draw, subtitle_wrapped, f_sub, W//2, P["subtitle_y"], fill=(255,255,255))

    # --- destino (grande, 200–240px fixos) ---
    draw_centered(draw, destination.upper(), f_dest, W//2, P["destination_y"], fill=accent_rgb, stroke_width=3)

    # --- preço à direita ---
    cx = P["price_center_x"]
    y0 = P["price_block_top_y"]
    draw_centered(draw, price_label.upper(), f_plab, cx, y0, fill=(255,255,255))
    _, hp = draw_centered(draw, price, f_price, cx, y0 + int(F["price_label"]*0.2), fill=accent_rgb, stroke_width=3)
    draw_centered(draw, price_by.upper(), f_pby, cx, y0 + int(F["price_label"]*0.2) + int(hp*0.75), fill=(255,255,255))

    # --- ícones e rodapé (mantidos iguais) ---
    icon_texts = [
        (f"{origin}\n{dates}", "✈️"),
        (hotel, "🏨"),
        (meal, "🍽️"),
        (baggage, "🧳"),
        (transfer, "🚐"),
    ]
    n = len(icon_texts)
    spacing = W // n
    for i, (txt, ic) in enumerate(icon_texts):
        xc = spacing * i + spacing//2
        draw_centered(draw, ic, f_icm, xc, P["icons_y"] - F["icons_emoji"], fill=accent_rgb)
        draw.multiline_text((xc - text_size(draw, txt.upper(), f_ic)[0]/2, P["icons_y"]),
                            txt.upper(), font=f_ic, fill=(255,255,255), align="center",
                            spacing=6, stroke_width=2, stroke_fill=(0,0,0))

    draw_centered(draw, "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES.", 
                  f_foot, W//2, P["footer_y"], fill=(255,255,255))

    # --- preview e download ---
    st.markdown("### Pré-visualização")
    st.image(canvas.convert("RGB"), use_container_width=True)

    buf = BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    st.download_button("⬇️ Fazer download do card (PNG)", data=buf.getvalue(), file_name=outfile_name)