import streamlit as st

st.title("📋 Painel do Atendente")
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

if 'senhas_pendentes' not in st.session_state:
    st.session_state.senhas_pendentes = {s: [] for s in setores}

if 'senhas_atendidas' not in st.session_state:
    st.session_state.senhas_atendidas = {s: [] for s in setores}

setor = st.selectbox("Selecione seu setor:", setores)

pendentes = st.session_state.senhas_pendentes[setor]
atendidas = st.session_state.senhas_atendidas[setor]

st.subheader(f"Senhas pendentes - {setor} ({len(pendentes)})")
if pendentes:
    idx_para_remover = None
    for idx, item in enumerate(pendentes):
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**{item['senha']}**")
        col2.write(f"Hora: {item['hora']}")
        if col3.button("Atender", key=f"atender_{setor}_{item['senha']}_{idx}"):
            idx_para_remover = idx

    if idx_para_remover is not None:
        # Move para atendidas
        atendida = pendentes.pop(idx_para_remover)
        atendidas.append(atendida)
        st.experimental_rerun()
else:
    st.info("Nenhuma senha em espera.")

st.markdown("---")
st.subheader(f"Senhas atendidas - {setor} ({len(atendidas)})")
for item in atendidas:
    st.write(f"**{item['senha']}** - {item['hora']}")
