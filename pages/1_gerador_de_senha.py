import streamlit as st
from datetime import datetime

st.title("📥 Gerador de Senhas")
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

if 'senhas' not in st.session_state:
    st.session_state.senhas = {s: [] for s in setores}

if 'contador' not in st.session_state:
    st.session_state.contador = {s: 0 for s in setores}

setor = st.selectbox("Selecione o setor para gerar a senha:", setores)

if st.button("Gerar Senha"):
    st.session_state.contador[setor] += 1
    nova = f"{setor[:2].upper()}-{st.session_state.contador[setor]:03}"
    st.session_state.senhas[setor].append({'senha': nova, 'hora': datetime.now().strftime('%H:%M:%S')})
    st.success(f"Senha gerada: **{nova}**")
