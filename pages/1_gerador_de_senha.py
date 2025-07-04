import streamlit as st
from datetime import datetime

st.title("📥 Gerador de Senhas")

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

# Inicialização dos dados se necessário
if 'senhas' not in st.session_state:
    st.session_state.senhas = {s: [] for s in setores}

if 'contador' not in st.session_state:
    st.session_state.contador = {s: 0 for s in setores}

# Tabs para escolher o tipo de geração
aba = st.radio("Escolha o modo de geração da senha:", ["🔁 Automática", "✍️ Manual"])

setor = st.selectbox("Selecione o setor de atendimento:", setores)

if aba == "🔁 Automática":
    if st.button("Gerar Senha Automática"):
        st.session_state.contador[setor] += 1
        senha = f"{setor[:2].upper()}-{st.session_state.contador[setor]:03}"
        st.session_state.senhas[setor].append({'senha': senha, 'hora': datetime.now().strftime('%H:%M:%S')})
        st.success(f"Senha gerada automaticamente: **{senha}**")

elif aba == "✍️ Manual":
    senha_manual = st.text_input("Digite a senha do papel:", max_chars=10)

    if st.button("Enviar senha manual"):
        if senha_manual.strip() == "":
            st.warning("⚠️ Digite uma senha válida.")
        else:
            senha_formatada = senha_manual.strip().upper()
            st.session_state.senhas[setor].append({'senha': senha_formatada, 'hora': datetime.now().strftime('%H:%M:%S')})
            st.success(f"Senha manual enviada: **{senha_formatada}** para o setor **{setor}**")
