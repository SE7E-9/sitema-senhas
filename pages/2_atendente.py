import streamlit as st

st.title("📋 Painel do Atendente")
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

# Verifica se existem senhas no estado
if 'senhas' not in st.session_state:
    st.session_state.senhas = {s: [] for s in setores}

# Escolhe o setor do atendente
setor = st.selectbox("Selecione seu setor:", setores)
fila = st.session_state.senhas[setor]

st.subheader(f"Senhas pendentes - {setor}")
if fila:
    for idx, item in enumerate(fila):
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**{item['senha']}**")
        col2.write(f"Hora: {item['hora']}")
        if col3.button("Atender", key=f"{setor}_{idx}"):
            st.session_state.senhas[setor].pop(idx)
            st.experimental_rerun()
else:
    st.info("Nenhuma senha em espera.")
