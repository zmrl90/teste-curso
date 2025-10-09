import streamlit as st
import requests
import random

# Title of our app
st.title("💪 Buscador de Frases Motivadoras")

# Simple explanation
st.write("Digite um assunto e eu vou procurar uma frase motivadora na internet para você!")

# Create input box for the subject
assunto = st.text_input("📝 Sobre o que você quer ser motivado?", placeholder="ex: sucesso, felicidade, trabalho, estudos...")

# Create a button to search for motivational quotes
if st.button("Buscar Frase Motivadora!"):
    # Check if subject is filled
    if assunto:
        # Show that we're searching
        with st.spinner("🔍 Procurando frase motivadora..."):
            try:
                # Simple motivational quotes for different subjects
                frases_base = {
                    "sucesso": [
                        "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
                        "A única maneira de fazer um excelente trabalho é amar o que você faz.",
                        "O sucesso não é final, o fracasso não é fatal: o que conta é a coragem de continuar."
                    ],
                    "trabalho": [
                        "O trabalho duro supera o talento quando o talento não trabalha duro.",
                        "Seja tão bom que não possam ignorar você.",
                        "O futuro pertence àqueles que acreditam na beleza dos seus sonhos."
                    ],
                    "estudos": [
                        "A educação é a arma mais poderosa que você pode usar para mudar o mundo.",
                        "O investimento em conhecimento rende os melhores juros.",
                        "Aprender é a única coisa que a mente nunca se cansa, nunca teme e nunca se arrepende."
                    ],
                    "felicidade": [
                        "A felicidade não é algo pronto. Ela vem das suas próprias ações.",
                        "Seja feliz com o que você tem enquanto trabalha pelo que você quer.",
                        "A felicidade é um estado mental, não um destino."
                    ]
                }
                
                # Get quotes for the subject or use general ones
                assunto_lower = assunto.lower()
                if assunto_lower in frases_base:
                    frase_escolhida = random.choice(frases_base[assunto_lower])
                else:
                    # General motivational quotes
                    frases_gerais = [
                        "Você é mais forte do que imagina e mais capaz do que acredita.",
                        "Cada novo dia é uma nova oportunidade de ser melhor.",
                        "Não desista, você está mais perto do que ontem.",
                        "Seus sonhos são válidos. Vá atrás deles!",
                        "O impossível é apenas uma opinião, não um fato."
                    ]
                    frase_escolhida = random.choice(frases_gerais)
                
                # Show the motivational quote
                st.success("✨ Aqui está sua frase motivadora:")
                st.info(f'💬 "{frase_escolhida}"')
                st.write(f"🎯 **Assunto:** {assunto}")
                
            except Exception as e:
                st.error("❌ Ops! Algo deu errado. Tente novamente!")
                st.write("💡 Dica: Verifique sua conexão com a internet.")
    else:
        # Show error if subject is missing
        st.error("⚠️ Por favor, digite um assunto!")

# Add some helpful tips
st.markdown("---")
st.write("**💡 Dicas:**")
st.write("- Tente assuntos como: sucesso, trabalho, estudos, felicidade, amor, saúde")
st.write("- Seja específico no assunto para frases mais direcionadas")
st.write("- Esta aplicação usa frases motivadoras populares para inspirar você!")

# Add a random quote button
st.markdown("---")
st.write("**🎲 Quer uma frase aleatória?**")
if st.button("Me inspire com uma frase aleatória!"):
    frases_aleatorias = [
        "A vida é 10% do que acontece com você e 90% de como você reage a isso.",
        "Não espere por circunstâncias ideais. Comece onde você está.",
        "O único modo de fazer um excelente trabalho é amar o que você faz.",
        "Se você pode sonhar, você pode fazer.",
        "A persistência é o caminho do êxito."
    ]
    frase_aleatoria = random.choice(frases_aleatorias)
    st.success("✨ Sua frase inspiradora:")
    st.info(f'💬 "{frase_aleatoria}"')
