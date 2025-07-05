import streamlit as st
import requests
from datetime import datetime

st.title("🎫 Gerador de Senhas")

api_pendentes = "https://api.sheetbest.com/sheets/f2bab54d-e790-46ea-9371-bd68e68bbcbc"

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
setor = st.selectbox("Selecione o setor:", setores)

with st.form("form_gerar"):
    senha_manual = st.text_input("Digite a senha manual (opcional):")
    enviar = st.form_submit_button("Gerar Senha")

    if enviar:
        # Buscar senhas já existentes
        try:
            res = requests.get(api_pendentes)
            if res.status_code != 200:
                st.error("Erro ao acessar a planilha online.")
                st.stop()
            senhas = res.json()
        except Exception as e:
            st.error(f"Erro na conexão: {e}")
            st.stop()

        # Gera nova senha
        if senha_manual.strip():
            nova_senha = senha_manual.strip()
        else:
            prefixo = setor[:2].upper()
            nova_senha = f"{prefixo}-{len(senhas)+1:03d}"

        payload = {
            "senha": nova_senha,
            "setor": setor,
            "hora": datetime.now().strftime("%H:%M:%S")
        }

        try:
            r = requests.post(api_pendentes, json=payload)
            if r.status_code == 200:
                st.success(f"Senha '{nova_senha}' gerada com sucesso!")
            else:
                st.error("Erro ao salvar a senha. Verifique a conexão.")
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
