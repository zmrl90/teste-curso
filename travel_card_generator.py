import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Gerador de Card - Viagens", 
    page_icon="🧳",
    layout="centered"
)

st.title("🧳 Gerador de Card de Viagem")
st.markdown("---")

# Explicação simples da aplicação
st.write("""
**Esta aplicação ajuda você a criar cards bonitos para promover viagens!**

Preencha as informações abaixo e clique em "Gerar Card" para criar seu card personalizado.
""")

# Criar um formulário organizado em seções
with st.form("card_form"):
    
    # Seção 1: Informações do Consultor
    st.subheader("👤 Informações do Consultor")
    col1, col2 = st.columns(2)
    
    with col1:
        consultor = st.text_input(
            "Nome do Consultor", 
            value="Consultor Independente RNAVT 3301",
            help="Digite o nome ou identificação do consultor"
        )
    
    with col2:
        empresa = st.text_input(
            "Nome da Empresa", 
            value="iCliGo Travel Consultant",
            help="Digite o nome da empresa de viagens"
        )
    
    st.markdown("---")
    
    # Seção 2: Informações do Destino
    st.subheader("🌍 Informações do Destino")
    
    subtitulo = st.text_input(
        "Frase de Apresentação", 
        value="Entre o sabor da pizza e a vista do Vesúvio – Nápoles encanta",
        help="Digite uma frase atrativa sobre o destino"
    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        destino = st.text_input(
            "Destino", 
            value="MALDIVAS",
            help="Nome do destino da viagem"
        )
    
    with col4:
        preco = st.text_input(
            "Preço", 
            value="409€",
            help="Preço da viagem (ex: 409€, 1.200€)"
        )
    
    st.markdown("---")
    
    # Seção 3: Detalhes da Viagem
    st.subheader("✈️ Detalhes da Viagem")
    
    col5, col6 = st.columns(2)
    
    with col5:
        cidade = st.text_input(
            "Cidade de Partida", 
            value="Lisboa",
            help="Cidade de onde a viagem parte"
        )
    
    with col6:
        datas = st.text_input(
            "Datas da Viagem", 
            value="7 a 15 Março",
            help="Período da viagem (ex: 7 a 15 Março)"
        )
    
    st.markdown("---")
    
    # Seção 4: Acomodação e Serviços
    st.subheader("🏨 Acomodação e Serviços")
    
    col7, col8 = st.columns(2)
    
    with col7:
        hotel = st.text_input(
            "Hotel", 
            value="OLEEEE",
            help="Nome do hotel da viagem"
        )
    
    with col8:
        regime = st.text_input(
            "Regime Alimentar", 
            value="Pequeno Almoço",
            help="Tipo de regime (ex: Pequeno Almoço, Meia Pensão, Pensão Completa)"
        )
    
    col9, col10 = st.columns(2)
    
    with col9:
        bagagem = st.text_input(
            "Bagagem", 
            value="Bagagem de mão",
            help="Tipo de bagagem incluída"
        )
    
    with col10:
        transfer = st.text_input(
            "Transfer", 
            value="Transfer In + Out",
            help="Serviços de transfer incluídos"
        )
    
    st.markdown("---")
    
    # Seção 5: Imagem de Fundo
    st.subheader("🖼️ Imagem de Fundo")
    
    imagem_bg = st.text_input(
        "URL da Imagem de Fundo",
        value="https://www.melhoresdestinos.com.br/wp-content/uploads/2020/12/quanto-custa-viajar-maldivas-capa2019-01.jpg",
        help="Cole aqui o link de uma imagem bonita do destino"
    )
    
    # Botão para gerar o card
    submit = st.form_submit_button("🎨 Gerar Card", type="primary")

# Geração do HTML quando o formulário é submetido
if submit:
    st.markdown("---")
    
    # Verificar se todos os campos obrigatórios foram preenchidos
    campos_obrigatorios = [subtitulo, destino, preco, cidade, datas, hotel, regime, bagagem, transfer]
    
    if all(campos_obrigatorios):
        st.success("✅ Card gerado com sucesso!")
        
        # Código HTML do card
        html_code = f"""
        <div style="position:relative;width:1080px;height:1440px;
                    background-image:url('{imagem_bg}');
                    background-size:1440px 1080px;background-position:center;
                    color:white;display:flex;flex-direction:column;
                    justify-content:space-between;text-align:center;">
          <div style="position:absolute;inset:0;background:rgba(0,0,0,0.4);"></div>

          <div style="position:relative;padding-top:2rem;">
            <p style="text-transform:uppercase;opacity:0.8;">{consultor}</p>
            <p style="font-weight:300;font-size:1.2rem;">{empresa}</p>
          </div>

          <div style="position:relative;margin-top:5rem;">
            <p style="text-transform:uppercase;letter-spacing:0.2em;margin-bottom:0.5rem;">{subtitulo}</p>
            <h1 style="font-size:5rem;font-weight:700;color:#00ffae;">{destino}</h1>
          </div>

          <div style="position:relative;margin-top:2rem;">
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


        # Mostrar a pré-visualização
        st.markdown("### 💻 Pré-visualização do Card:")
        st.components.v1.html(html_code, height=1200)
        

        
    else:
        st.error("❌ Por favor, preencha todos os campos obrigatórios!")
        st.info("💡 Todos os campos são necessários para criar o card. Verifique se não deixou nenhum vazio.")

# Rodapé com dicas
st.markdown("---")
st.caption("""
💡 **Dicas para usar a aplicação:**
- Use letras maiúsculas para o destino para melhor resultado visual
- Para a imagem de fundo, procure por fotos bonitas do destino no Google Imagens
- Você pode copiar o código HTML gerado para usar em outros lugares
- O card é otimizado para redes sociais e apresentações
""")
