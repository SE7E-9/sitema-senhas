import streamlit as st

st.title("📋 Painel do Atendente")
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

# Garante que as estruturas existam
if 'senhas' not in st.session_state:
    st.session_state.senhas = {s: [] for s in setores}

setor = st.selectbox("Selecione seu setor:", setores)
fila = st.session_state.senhas.get(setor, [])

st.subheader(f"Senhas pendentes - {setor}")

if fila:
    # Exibe senhas com botão para atendimento
    for idx in range(len(fila)):
        item = fila[idx]
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**{item['senha']}**")
        col2.write(f"Hora: {item['hora']}")

        # Criar uma chave única para o botão
        if col3.button("Atender", key=f"atender_{setor}_{item['senha']}_{idx}"):
            fila.pop(idx)
            st.success(f"Senha **{item['senha']}** atendida.")
            st.experimental_rerun()
            break
else:
    st.info("Nenhuma senha em espera.")
