import streamlit as st
import requests

st.title("📋 Painel do Atendente")

# URLs das APIs
api_pendentes = "https://api.sheetbest.com/sheets/f2bab54d-e790-46ea-9371-bd68e68bbcbc"
api_atendidas = "https://api.sheetbest.com/sheets/bb970f05-0342-4667-8fd4-8c16998c7422"

# Setores e atendentes
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Financeiro A', 'Financeiro B', 'Financeiro C'],
    'Protocolo': ['Protocolo A', 'Protocolo B'],
    'Geral': ['Geral Único']
}

# Seleção de setor e atendente
setor = st.selectbox("Selecione o setor:", setores)
atendente = st.selectbox("Selecione seu nome:", atendentes[setor])

# Botão de atualização manual
if st.button("🔄 Atualizar lista"):
    st.experimental_rerun()

# Obter senhas pendentes
try:
    res = requests.get(api_pendentes)
    senhas = res.json()
    senhas_do_setor = [s for s in senhas if s.get("setor") == setor]
except Exception as e:
    st.error(f"Erro ao buscar senhas: {e}")
    senhas_do_setor = []

st.subheader(f"Senhas Pendentes - {setor}")

# Exibir senhas
if not senhas_do_setor:
    st.info("Nenhuma senha pendente.")
else:
    for senha in senhas_do_setor:
        if "id" not in senha or not senha["id"]:
            continue  # Ignora senhas antigas sem ID

        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{senha.get('senha', '—')}**")
        col2.write(f"{senha.get('hora', '—')}")
        
        if col3.button("Atender", key=senha["id"]):
            payload = {
                "id": senha["id"],
                "senha": senha["senha"],
                "setor": senha["setor"],
                "hora": senha["hora"],
                "atendente": atendente
            }

            try:
                # Salvar na aba Atendidas
                r = requests.post(api_atendidas, json=payload)
                if r.status_code != 200:
                    st.error("Erro ao salvar em atendidas.")
                    st.stop()

                # Apagar da aba Pendentes
                r2 = requests.delete(f"{api_pendentes}?id={senha['id']}")
                if r2.status_code == 200:
                    st.success(f"Senha {senha['senha']} atendida.")
                    st.experimental_rerun()
                else:
                    st.error("Erro ao remover da lista.")
            except Exception as e:
                st.error(f"Erro ao atender: {e}")

# Exibir últimas atendidas
st.markdown("---")
st.subheader("Últimas Senhas Atendidas")

try:
    r = requests.get(api_atendidas)
    atendidas = [s for s in r.json() if s.get("setor") == setor]
    for s in atendidas[::-1][:10]:
        st.write(f"**{s.get('senha', '—')}** - {s.get('hora', '—')} - 👤 {s.get('atendente', '—')}")
except:
    st.warning("Não foi possível carregar atendimentos recentes.")
