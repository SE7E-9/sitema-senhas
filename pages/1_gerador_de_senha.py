import streamlit as st
import requests
from datetime import datetime

st.title("🎫 Gerador de Senhas")

setores = ['Veículos', 'Taxas Licenciamento', 'Multas//Liberação', 'Despachante']

api_pendentes = "https://api.sheetbest.com/sheets/f2bab54d-e790-46ea-9371-bd68e68bbcbc"

setor = st.selectbox("Selecione o setor:", setores)

with st.form("form_gerar_senha"):
    senha_manual = st.text_input("Digite a senha manual (ou deixe vazio para gerar automática):")
    enviar = st.form_submit_button("Gerar senha")

    if enviar:
        # Buscar todas as senhas já inseridas
        resposta = requests.get(api_pendentes)
        dados = resposta.json()
        total = len(dados)

        if senha_manual.strip():
            nova_senha = senha_manual.strip()
        else:
            prefixo = setor[:2].upper()
            nova_senha = f"{prefixo}-{total+1:03d}"

        payload = {
            "senha": nova_senha,
            "setor": setor,
            "hora": datetime.now().strftime("%H:%M:%S")
        }

        r = requests.post(api_pendentes, json=payload)

        if r.status_code == 200:
            st.success(f"Senha '{nova_senha}' gerada com sucesso para o setor {setor}!")
        else:
            st.error("Erro ao salvar a senha. Verifique a conexão.")
