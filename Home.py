import streamlit as st

st.set_page_config(page_title="Sistema de Senhas", layout="centered")

st.title("🎫 Sistema de Senhas por Setor")
st.markdown("---")

st.markdown("Use o menu lateral para escolher entre:")
st.markdown("- 📥 **Gerador de Senhas** para recepção ou autoatendimento")
st.markdown("- 📋 **Atendente** para visualizar e chamar senhas por setor")

# Inicialização das listas de senhas pendentes e atendidas
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

if 'senhas_pendentes' not in st.session_state:
    st.session_state.senhas_pendentes = {s: [] for s in setores}

if 'senhas_atendidas' not in st.session_state:
    st.session_state.senhas_atendidas = {s: [] for s in setores}
