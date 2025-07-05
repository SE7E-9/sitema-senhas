import streamlit as st
from datetime import datetime

st.title("🎫 Gerador de Senhas")

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

# Inicializa os dicionários no session_state
if 'senhas_pendentes' not in st.session_state:
    st.session_state.senhas_pendentes = {s: [] for s in setores}
if 'senhas_atendidas' not in st.session_state:
    st.session_state.senhas_atendidas = {s: [] for s in setores}

setor = st.selectbox("Selecione o setor:", setores)

with st.form("form_gerar_senha"):
    senha_manual = st.text_input("Digite a senha manual (ou deixe vazio para gerar automática):")
    enviar = st.form_submit_button("Gerar senha")

    def gerar_senha_automatica(setor):
        total = len(st.session_state.senhas_pendentes[setor]) + len(st.session_state.senhas_atendidas[setor])
        prefixo = setor[:2].upper()
        numero = total + 1
        return f"{prefixo}-{numero:03d}"

    if enviar:
        if senha_manual.strip():
            nova_senha = senha_manual.strip()
        else:
            nova_senha = gerar_senha_automatica(setor)

        registro = {
            'senha': nova_senha,
            'hora': datetime.now().strftime("%H:%M:%S")
        }

        st.session_state.senhas_pendentes[setor].append(registro)
        st.success(f"Senha '{nova_senha}' gerada para o setor {setor}!")

# Exibir senhas pendentes
st.subheader(f"Senhas pendentes para {setor} ({len(st.session_state.senhas_pendentes[setor])})")
if st.session_state.senhas_pendentes[setor]:
    for item in st.session_state.senhas_pendentes[setor]:
        st.write(f"**{item['senha']}** - {item['hora']}")
else:
    st.info("Nenhuma senha pendente.")
