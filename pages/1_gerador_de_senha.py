import streamlit as st
from datetime import datetime

st.title("🎫 Gerador de Senhas")

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']

# Inicializa as listas no session_state, se ainda não existirem
if 'senhas_pendentes' not in st.session_state:
    st.session_state.senhas_pendentes = {s: [] for s in setores}

if 'senhas_atendidas' not in st.session_state:
    st.session_state.senhas_atendidas = {s: [] for s in setores}

# Seleção do setor para gerar a senha
setor = st.selectbox("Selecione o setor:", setores)

# Entrada para senha manual (opcional)
senha_manual = st.text_input("Digite a senha manual (deixe vazio para gerar automática):")

def gerar_senha_automatica(setor):
    # Conta quantas senhas pendentes + atendidas já foram geradas para criar sequência
    total_geradas = len(st.session_state.senhas_pendentes[setor]) + len(st.session_state.senhas_atendidas[setor])
    prefixo = setor[:2].upper()
    numero = total_geradas + 1
    return f"{prefixo}-{numero:03d}"

if st.button("Gerar senha"):
    if senha_manual.strip():
        nova_senha = senha_manual.strip()
    else:
        nova_senha = gerar_senha_automatica(setor)

    # Cria o registro da senha com horário
    registro = {
        'senha': nova_senha,
        'hora': datetime.now().strftime("%H:%M:%S")
    }

    st.session_state.senhas_pendentes[setor].append(registro)
    st.success(f"Senha '{nova_senha}' gerada para o setor {setor}!")

st.subheader(f"Senhas pendentes para {setor} ({len(st.session_state.senhas_pendentes[setor])})")
if st.session_state.senhas_pendentes[setor]:
    for item in st.session_state.senhas_pendentes[setor]:
        st.write(f"**{item['senha']}** - {item['hora']}")
else:
    st.info("Nenhuma senha pendente.")

