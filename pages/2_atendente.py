import streamlit as st
import requests

st.title("📋 Painel do Atendente")

api_pendentes = "https://api.sheetbest.com/sheets/f2bab54d-e790-46ea-9371-bd68e68bbcbc"
api_atendidas = "https://api.sheetbest.com/sheets/bb970f05-0342-4667-8fd4-8c16998c7422"

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Financeiro A', 'Financeiro B', 'Financeiro C'],
    'Protocolo': ['Protocolo A', 'Protocolo B'],
    'Geral': ['Geral Único']
}

setor = st.selectbox("Selecione o setor:", setores)
atendente = st.selectbox("Selecione seu nome:", atendentes[setor])

# Botão de atualização manual
if st.button("🔄 Atualizar lista"):
    st.experimental_rerun()

# Obter senhas pendentes
try:
    res = requests.get(api_pendentes)
    senhas = res.json()
    senhas_do_setor = [s for s in senhas if s["setor"] == setor]
except Exception as e:
    st.error(f"Erro ao buscar senhas: {e}")
    senhas_do_setor = []

st.subheader(f"Senhas Pendentes - {setor}")

if not senhas_do_setor:
    st.info("Nenhuma senha pendente.")
else:
    for senha in senhas_do_setor:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{senha['senha']}**")
        col2.write(f"{senha['hora']}")
        if col3.button("Atender", key=senha['senha']):
            payload = {
                "senha": senha["senha"],
                "setor": senha["setor"],
                "hora": senha["hora"],
                "atendente": atendente
            }

            try:
                # Enviar para atendidas
                r = requests.post(api_atendidas, json=payload)
                if r.status_code != 200:
                    st.error("Erro ao mover para atendidas.")
                    st.stop()

                # Remover da pendente
                url_delete = f"{api_pendentes}?senha={senha['senha']}&setor={senha['setor']}&hora={senha['hora']}"
                r2 = requests.delete(url_delete)
                if r2.status_code == 200:
                    st.success(f"Senha {senha['senha']} atendida por {atendente}")
                    st.experimental_rerun()
                else:
                    st.error("Erro ao remover senha da lista.")
            except Exception as e:
                st.error(f"Erro ao atender: {e}")
                st.stop()

# Mostrar últimas atendidas
st.markdown("---")
st.subheader("Últimas Senhas Atendidas")

try:
    r = requests.get(api_atendidas)
    atendidas = [s for s in r.json() if s["setor"] == setor]
    for s in atendidas[::-1][:10]:
        st.write(f"**{s['senha']}** - {s['hora']} - 👤 {s.get('atendente', '—')}")
except:
    st.warning("Não foi possível carregar atendimentos recentes.")
