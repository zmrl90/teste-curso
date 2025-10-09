#!/usr/bin/env python3
"""
Script simples para executar o Instagram Analyzer
"""

import subprocess
import sys
import os

def main():
    """Executa o Instagram Analyzer"""
    print("🚀 Iniciando Instagram Analyzer...")
    print("📝 Esta aplicação simula a análise de perfis do Instagram")
    print("🌐 A aplicação abrirá no seu navegador")
    print("-" * 50)
    
    # Verifica se o arquivo existe
    if not os.path.exists("instagram_analyzer.py"):
        print("❌ Erro: arquivo instagram_analyzer.py não encontrado!")
        return
    
    try:
        # Executa o streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "instagram_analyzer.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar a aplicação: {e}")
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")

if __name__ == "__main__":
    main()
