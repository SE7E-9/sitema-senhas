import streamlit as st
import requests
from datetime import datetime
import uuid

st.set_page_config(page_title="Gerador de Senhas", layout="centered")
st.title("🎫 Gerador de Senhas")

api_pendentes = "https://api.sheetbest.com/sheets/2293ec75-0867-4721-ada5-8e7525c96351"

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
setor = st.selectbox("Selecione o setor:", setores)

if "senha_manual" not in st.session_state:
    st.session_state.senha_manual = ""

with st.form("form_gerar"):
    senha_manual = st.text_input("Digite a senha manual (opcional):", value=st.session_state.senha_manual)
    enviar = st.form_submit_button("Gerar Senha")

    if enviar:
        try:
            res = requests.get(api_pendentes)
            res.raise_for_status()
            senhas = res.json()
        except Exception as e:
            st.error(f"Erro ao acessar a planilha: {e}")
            st.stop()

        nova_senha = senha_manual.strip() if senha_manual.strip() else f"{setor[:2].upper()}-{len(senhas)+1:03d}"
        id_unico = str(uuid.uuid4())

        payload = {
            "id": id_unico,
            "senha": nova_senha,
            "setor": setor.strip().title(),
            "hora": datetime.now().strftime("%H:%M:%S")
        }

        try:
            r = requests.post(api_pendentes, json=payload)
            r.raise_for_status()
            st.success(f"✅ Senha '{nova_senha}' gerada com sucesso para o setor **{setor}**.")
            st.session_state.senha_manual = ""
        except Exception as e:
            st.error(f"Erro ao salvar a senha: {e}")
