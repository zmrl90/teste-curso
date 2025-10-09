import streamlit as st
import random

# Título da aplicação
st.title("📸 Instagram Analyzer")

# Explicação simples
st.write("Esta aplicação simula a análise de um perfil do Instagram para criar publicações no mesmo estilo!")

# Input para o perfil do Instagram
instagram_profile = st.text_input("🔍 Digite o nome do perfil do Instagram:", placeholder="exemplo: @fotografo_brasil")

# Botão para analisar
if st.button("Analisar Perfil"):
    if instagram_profile:
        # Simula a análise do perfil
        st.success(f"✅ Analisando perfil: {instagram_profile}")
        
        # Simula descobertas sobre o perfil
        st.write("**🔍 Análise do perfil:**")
        
        # Simula temas encontrados
        temas = ["natureza", "viagem", "comida", "lifestyle", "moda", "arte"]
        tema_principal = random.choice(temas)
        
        st.write(f"• Tema principal: {tema_principal}")
        st.write("• Estilo: Fotos com cores vibrantes")
        st.write("• Frequência: 2-3 posts por semana")
        st.write("• Horários: Manhã e final da tarde")
        
        # Simula análise de hashtags
        st.write("\n**📝 Hashtags mais usadas:**")
        hashtags_exemplo = ["#fotografia", "#natureza", "#brasil", "#vida", "#momento"]
        for hashtag in hashtags_exemplo:
            st.write(f"• {hashtag}")
        
        # Gera uma sugestão de post
        st.write("\n**✨ Sugestão de nova publicação:**")
        
        # Simula diferentes tipos de posts baseados no tema
        sugestoes = {
            "natureza": "🌿 Post sobre um pôr do sol em uma praia deserta",
            "viagem": "✈️ Foto de uma cidade histórica com arquitetura única",
            "comida": "🍕 Receita caseira de um prato tradicional",
            "lifestyle": "☕ Momento de relaxamento em casa com um bom livro",
            "moda": "👗 Look casual para um dia de passeio",
            "arte": "🎨 Processo criativo de uma pintura abstrata"
        }
        
        sugestao = sugestoes.get(tema_principal, "📸 Uma foto que representa seu estilo único")
        st.info(sugestao)
        
        # Simula legenda sugerida
        st.write("**📝 Legenda sugerida:**")
        legendas = [
            "Cada momento é uma oportunidade de criar memórias incríveis ✨",
            "A beleza está nos detalhes que muitas vezes passam despercebidos 🌟",
            "Hoje foi um daqueles dias que ficam marcados para sempre 💫",
            "A vida é feita de pequenos momentos que se tornam grandes lembranças 🌈"
        ]
        legenda_sugerida = random.choice(legendas)
        st.write(f'"{legenda_sugerida}"')
        
        # Hashtags sugeridas
        st.write("\n**#️⃣ Hashtags sugeridas:**")
        hashtags_sugeridas = hashtags_exemplo + [f"#{tema_principal}", "#instagood", "#fotografia"]
        st.write(" ".join(hashtags_sugeridas))
        
        # Botão para gerar nova sugestão
        if st.button("🔄 Gerar Nova Sugestão"):
            st.rerun()
            
    else:
        st.error("⚠️ Por favor, digite o nome do perfil do Instagram!")

# Informações adicionais
st.markdown("---")
st.write("**💡 Como funciona:**")
st.write("1. A aplicação analisa o perfil fornecido")
st.write("2. Identifica padrões nas publicações existentes")
st.write("3. Cria sugestões baseadas no estilo encontrado")
st.write("4. Gera legendas e hashtags no mesmo padrão")

st.write("\n**📚 Nota para aprendizado:**")
st.write("Esta é uma versão simplificada para demonstrar o conceito. Em uma aplicação real, você usaria:")
st.write("- APIs do Instagram para acessar dados reais")
st.write("- Inteligência Artificial para análise de imagens")
st.write("- Processamento de linguagem natural para entender legendas")
