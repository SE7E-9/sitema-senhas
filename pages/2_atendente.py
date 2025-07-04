import streamlit as st

st.title("📋 Painel do Atendente")
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

if 'senhas' not in st.session_state:
    st.session_state.senhas = {s: [] for s in setores}

setor = st.selectbox("Selecione seu setor:", setores)
fila = st.session_state.senhas.get(setor, [])

st.subheader(f"Senhas pendentes - {setor}")

# Guardar índice para remover fora do loop
idx_para_remover = None

if fila:
    for idx, item in enumerate(fila):
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**{item['senha']}**")
        col2.write(f"Hora: {item['hora']}")
        if col3.button("Atender", key=f"atender_{setor}_{item['senha']}_{idx}"):
            idx_para_remover = idx

    # Remove e rerun fora do loop
    if idx_para_remover is not None:
        fila.pop(idx_para_remover)
        st.experimental_rerun()
else:
    st.info("Nenhuma senha em espera.")
