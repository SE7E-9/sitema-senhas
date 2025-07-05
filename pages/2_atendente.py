import streamlit as st

st.title("📋 Painel do Atendente")

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes_por_setor = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Atendente A', 'Atendente B', 'Atendente C'],
    'Protocolo': ['Atendente X', 'Atendente Y'],
    'Geral': ['Atendente Único']
}

if 'senhas_pendentes' not in st.session_state:
    st.session_state.senhas_pendentes = {s: [] for s in setores}
if 'senhas_atendidas' not in st.session_state:
    st.session_state.senhas_atendidas = {s: [] for s in setores}

setor = st.selectbox("Selecione seu setor:", setores)
atendente = st.selectbox("Selecione seu nome:", atendentes_por_setor[setor])

pendentes = st.session_state.senhas_pendentes[setor]
atendidas = st.session_state.senhas_atendidas[setor]

st.subheader(f"Senhas pendentes - {setor} ({len(pendentes)})")

# Variável para remover após o loop
idx_para_remover = None

if pendentes:
    for idx, item in enumerate(pendentes):
        col1, col2, col3 = st.columns([2,2,1])
        col1.write(f"**{item['senha']}**")
        col2.write(f"Hora: {item['hora']}")
        if col3.button("Atender", key=f"atender_{setor}_{item['senha']}_{idx}"):
            idx_para_remover = idx

    # Remove a senha fora do loop e então atualiza a página
    if idx_para_remover is not None:
        atendida = pendentes.pop(idx_para_remover)
        atendida['atendente'] = atendente
        atendidas.append(atendida)
        st.experimental_rerun()
else:
    st.info("Nenhuma senha em espera.")

st.markdown("---")
st.subheader(f"Senhas atendidas - {setor} ({len(atendidas)})")
for item in atendidas:
    st.write(f"**{item['senha']}** - {item['hora']} - Atendido por: {item.get('atendente', 'Desconhecido')}")
