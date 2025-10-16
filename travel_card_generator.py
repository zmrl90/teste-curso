import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags
import requests
from io import BytesIO
import textwrap

st.set_page_config(page_title="Gerador de Card - Viagens", layout="centered")

# --------------------
# URLs de fontes (2 CDNs)
# --------------------
FONT_SOURCES = {
    "regular": [
        "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-Regular.ttf",
        "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat-Regular.ttf",
    ],
    "semibold": [
        "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-SemiBold.ttf",
        "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat-SemiBold.ttf",
    ],
    "bold": [
        "https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat-Bold.ttf",
        "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/montserrat/Montserrat-Bold.ttf",
    ],
}

# --------------------
# Helpers
# --------------------
@st.cache_data(show_spinner=False)
def download_bytes(url, timeout=12):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.content
    except Exception:
        return None

def try_load_truetype_from_urls(url_list, size):
    for url in url_list:
        data = download_bytes(url)
        if data:
            try:
                return ImageFont.truetype(BytesIO(data), size=size)
            except Exception:
                continue
    return None  # NÃO voltar ao load_default()

def resolve_font(style_key, size, uploads):
    """
    Resolve a fonte pelo upload (se existir) ou pelos CDNs.
    Se falhar, retorna None (para abortar com mensagem clara).
    """
    uploaded = uploads.get(style_key)
    if uploaded is not None:
        try:
            return ImageFont.truetype(uploaded, size=size)
        except Exception:
            st.warning(f"Não foi possível ler a fonte carregada para {style_key}. Vou tentar CDN.")
    # Tentar CDNs
    f = try_load_truetype_from_urls(FONT_SOURCES[style_key], size)
    return f

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered(draw, text, font, x_center, y, fill=(255, 255, 255),
                  align="center", stroke_width=0, stroke_fill=(0, 0, 0)):
    w, h = text_size(draw, text, font)
    draw.text((x_center - w / 2, y), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)
    return w, h

def fix_exif_orientation(img: Image.Image) -> Image.Image:
    try:
        exif = img._getexif()
        if not exif:
            return img
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                o = exif.get(orientation, None)
                if o == 3:  return img.rotate(180, expand=True)
                if o == 6:  return img.rotate(270, expand=True)
                if o == 8:  return img.rotate(90, expand=True)
                break
    except Exception:
        pass
    return img

def cover_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    ratio_img = img.width / img.height
    ratio_tar = target_w / target_h
    if ratio_img > ratio_tar:
        new_h = target_h
        new_w = int(ratio_img * new_h)
    else:
        new_w = target_w
        new_h = int(new_w / ratio_img)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))

def fit_font_to_block(draw, text, bold_sources, target_height, max_width,
                      min_size=40, max_size=400, uploads=None):
    lo, hi = min_size, max_size
    best = resolve_font("bold", lo, uploads)
    if best is None:
        return None
    while lo <= hi:
        mid = (lo + hi) // 2
        f = resolve_font("bold", mid, uploads)
        if f is None:
            return None
        w, h = text_size(draw, text, f)
        if h <= target_height and w <= max_width:
            best = f
            lo = mid + 1
        else:
            hi = mid - 1
    return best

# --------------------
# UI
# --------------------
st.title("🧳 Gerador de Card de Viagem (template: NÁPOLES)")

with st.form("inputs"):
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Conteúdo do Card")
        subtitle = st.text_input("Subtítulo", "Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta")
        destination = st.text_input("Destino (grande)", "NÁPOLES")
        price = st.text_input("Preço", "409€")
        price_label = st.text_input("Preço - rótulo acima (ex: Desde)", "DESDE")
        price_by = st.text_input("Texto abaixo do preço", "POR PESSOA")

        st.write("---")
        st.write("Detalhes (linha de ícones)")
        origin = st.text_input("Cidade de Partida", "Porto")
        dates = st.text_input("Datas", "7 a 15 Março")
        hotel = st.text_input("Hotel", "Hotel Herculaneum")
        meal = st.text_input("Regime", "Pequeno Almoço")
        baggage = st.text_input("Bagagem", "Bagagem de mão")
        transfer = st.text_input("Transfer", "Transfer In + Out")

    with col_b:
        st.subheader("Imagem e formato")
        input_mode = st.radio("Fonte da imagem de fundo", ("Upload local", "URL"), index=0)
        if input_mode == "Upload local":
            upload = st.file_uploader("Carrega uma imagem (jpg/png)", type=["jpg", "jpeg", "png"])
            image_url = ""
        else:
            upload = None
            image_url = st.text_input(
                "URL da imagem",
                "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1400&auto=format&fit=crop"
            )

        st.write("---")
        fmt = st.selectbox("Formato da imagem", ("Feed 1080×1350", "Quadrado 1080×1080", "Wide 1920×1080", "Story 1080×1920"), index=0)
        outfile_name = st.text_input("Nome do ficheiro para download", "card_viagem.png")
        color_accent = st.color_picker("Cor de destaque (texto & ícones)", "#00ffae")

        st.write("---")
        scale = st.slider("Tamanho do texto (escala global)", 0.8, 3.0, 2.0, 0.1)

        st.caption("⚙️ Se necessário, faz upload das fontes Montserrat (TTF):")
        f_upload_reg = st.file_uploader("Montserrat-Regular.ttf (opcional)", type=["ttf"], key="freg")
        f_upload_sem = st.file_uploader("Montserrat-SemiBold.ttf (opcional)", type=["ttf"], key="fsem")
        f_upload_bold = st.file_uploader("Montserrat-Bold.ttf (opcional)", type=["ttf"], key="fbold")

    submit = st.form_submit_button("🎨 Gerar e Pré-visualizar")

# --------------------
# Render
# --------------------
if submit:
    # Tamanho por formato
    if fmt == "Feed 1080×1350":
        W, H = 1080, 1350
    elif fmt == "Quadrado 1080×1080":
        W, H = 1080, 1080
    elif fmt == "Wide 1920×1080":
        W, H = 1920, 1080
    else:
        W, H = 1080, 1920

    # Carregar fundo
    try:
        if upload is not None:
            bg = Image.open(upload)
        else:
            data = download_bytes(image_url, timeout=15)
            if not data:
                raise RuntimeError("Falha ao fazer download da imagem.")
            bg = Image.open(BytesIO(data))
        bg = fix_exif_orientation(bg).convert("RGBA")
    except Exception as e:
        st.error(f"Erro ao carregar imagem de fundo: {e}")
        st.stop()

    # Ajustar imagem (cover)
    bg = cover_resize(bg, W, H)

    # Overlay escuro e base do desenho
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    canvas = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(canvas)

    # Cor de destaque
    accent_rgb = tuple(int(color_accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    # Map uploads
    uploads = {"regular": f_upload_reg, "semibold": f_upload_sem, "bold": f_upload_bold}

    # ======== CARREGAR FONTES (ABORTAR SE FALHAREM) ========
    f_top   = resolve_font("regular", int(34 * scale), uploads)
    f_sub   = resolve_font("semibold", int(54 * scale), uploads)
    f_price = resolve_font("bold",    int(360 * scale), uploads)
    f_plab  = resolve_font("semibold", int(72 * scale), uploads)
    f_pby   = resolve_font("regular",  int(60 * scale), uploads)
    f_icon  = resolve_font("regular",  int(58 * scale), uploads)
    f_emoji = resolve_font("semibold", int(86 * scale), uploads)
    f_foot  = resolve_font("regular",  int(40 * scale), uploads)

    required = [("Topo", f_top), ("Subtítulo", f_sub), ("Preço", f_price),
                ("Rótulo preço", f_plab), ("Texto abaixo preço", f_pby),
                ("Ícones texto", f_icon), ("Ícones emoji", f_emoji), ("Rodapé", f_foot)]
    missing = [name for name, f in required if f is None]
    if missing:
        st.error("Não foi possível carregar as fontes TrueType para: " + ", ".join(missing) +
                 ". Faz upload das TTF ou verifica a ligação aos CDNs.")
        st.stop()
    # =======================================================

    # Topo
    top_y = int(28 * scale)
    draw_centered(draw, "CONSULTOR INDEPENDENTE RNAVT3301", f_top, W // 2, top_y, fill=(255, 255, 255))
    draw_centered(draw, "iCliGo travel consultant", f_top, W // 2, top_y + int(48 * scale), fill=(255, 255, 255))

    # Subtítulo
    subtitle_y = 260 if fmt == "Feed 1080×1350" else (220 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 360)
    subtitle_wrapped = "\n".join(textwrap.wrap(subtitle.upper(), width=38))
    draw_centered(draw, subtitle_wrapped, f_sub, W // 2, subtitle_y, fill=(255, 255, 255),
                  stroke_width=2, stroke_fill=(0, 0, 0))

    # DESTINO (auto-fit num bloco de 200px)
    dest_text = destination.upper()
    block_height = 200
    block_top = 380 if fmt == "Feed 1080×1350" else (320 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 520)
    block_center_y = block_top + block_height // 2

    f_dest = fit_font_to_block(draw, dest_text, FONT_SOURCES["bold"],
                               target_height=block_height, max_width=int(W * 0.9),
                               min_size=80, max_size=420, uploads=uploads)
    if f_dest is None:
        st.error("Não consegui carregar a fonte para o DESTINO. Faz upload da Montserrat-Bold.ttf.")
        st.stop()

    w_dest, h_dest = text_size(draw, dest_text, f_dest)
    dest_y = block_center_y - h_dest // 2
    draw.text((W/2 - w_dest/2, dest_y), dest_text, font=f_dest,
              fill=accent_rgb, stroke_width=3, stroke_fill=(0, 0, 0))

    # Preço (direita)
    price_cx = int(W * 0.72)
    price_top = 720 if fmt == "Feed 1080×1350" else (610 if fmt.startswith("Quadrado") else (560 if fmt.startswith("Wide") else 980))
    draw_centered(draw, price_label.upper(), f_plab, price_cx, price_top, fill=(255, 255, 255))
    _, hp = draw_centered(draw, price, f_price, price_cx, price_top + int(20 * scale),
                          fill=accent_rgb, stroke_width=3, stroke_fill=(0, 0, 0))
    draw_centered(draw, price_by.upper(), f_pby, price_cx,
                  price_top + int(20 * scale) + int(hp * 0.75),
                  fill=(255, 255, 255))

    # Ícones / detalhes
    icons_y = 1020 if fmt == "Feed 1080×1350" else (840 if fmt.startswith("Quadrado") else (860 if fmt.startswith("Wide") else 1460))
    icon_texts = [
        (f"{origin}\n{dates}", "✈️"),
        (f"HOTEL\n{hotel}", "🏨"),
        (meal, "🍽️"),
        (baggage, "🧳"),
        (transfer, "🚐"),
    ]
    n = len(icon_texts)
    spacing = W // n
    for i, (txt, ic) in enumerate(icon_texts):
        xc = spacing * i + spacing // 2
        draw_centered(draw, ic, f_emoji, xc, icons_y - int(64 * scale), fill=accent_rgb)
        lines = txt.upper()
        w_lbl, _ = text_size(draw, lines, f_icon)
        draw.multiline_text((xc - w_lbl/2, icons_y), lines, font=f_icon, fill=(255, 255, 255),
                            align="center", spacing=int(8 * scale), stroke_width=2, stroke_fill=(0, 0, 0))

    # Rodapé
    footer_y = 1280 if fmt == "Feed 1080×1350" else (1000 if fmt.startswith("Quadrado") or fmt.startswith("Wide") else 1820)
    footer_text = "VALOR BASEADO EM 2 ADULTOS. PREÇOS SUJEITOS A ALTERAÇÕES."
    draw_centered(draw, footer_text, f_foot, W // 2, footer_y, fill=(255, 255, 255))

    # Preview e download
    st.markdown("### Pré-visualização")
    st.image(canvas.convert("RGB"), use_container_width=True)

    buf = BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    st.download_button("⬇️ Fazer download do card (PNG)", data=buf, file_name=outfile_name or "card_viagem.png", mime="image/png")

    st.success("✅ Card gerado. (Se o texto ainda parecer pequeno, aumenta a 'Escala do texto'.)")
