import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Painel do Atendente", layout="centered")
st.title("📋 Painel do Atendente")

# Atualização automática
st_autorefresh(interval=10_000, key="refresh")

# NOVOS LINKS das planilhas
api_pendentes = "https://api.sheetbest.com/sheets/c424cb40-ac76-4fdd-ae6f-7a99f4bc77fe"
api_atendidas = "https://api.sheetbest.com/sheets/85deb476-3818-459c-9208-e0f41516d286"

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes_por_setor = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Financeiro A', 'Financeiro B', 'Financeiro C'],
    'Protocolo': ['Protocolo A', 'Protocolo B'],
    'Geral': ['Geral Único']
}

setor = st.selectbox("Selecione o setor:", setores)
atendente = st.selectbox("Selecione seu nome:", atendentes_por_setor[setor])

try:
    res = requests.get(api_pendentes)
    res.raise_for_status()
    todas = res.json()
except Exception as e:
    st.error(f"Erro ao carregar senhas pendentes: {e}")
    todas = []

senhas_do_setor = [s for s in todas if s.get("setor", "").strip().lower() == setor.lower()]

st.subheader(f"🎟️ Senhas Pendentes - {setor}")

if not senhas_do_setor:
    st.info("Nenhuma senha pendente no momento.")
else:
    for senha in senhas_do_setor:
        if not senha.get("id"):
            continue
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.markdown(f"**{senha.get('senha', '—')}**")
        col2.markdown(f"{senha.get('hora', '—')}")
        if col3.button("Atender", key=senha["id"]):
            payload = {
                "id": senha["id"],
                "senha": senha["senha"],
                "setor": senha["setor"],
                "hora": senha["hora"],
                "atendente": atendente
            }
            try:
                requests.post(api_atendidas, json=payload).raise_for_status()
                requests.delete(f"{api_pendentes}?id={senha['id']}").raise_for_status()
                st.success(f"✅ Senha {senha['senha']} atendida por {atendente}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao registrar atendimento: {e}")

def atendente_preenchido(senha):
    atendente_valor = senha.get("atendente")
    return isinstance(atendente_valor, str) and atendente_valor.strip().lower() not in ["", "-", "nenhum", "vazio"]

st.markdown("---")
st.subheader("📚 Últimos Atendimentos")

try:
    res = requests.get(api_atendidas)
    res.raise_for_status()
    historico = res.json()
    historico = [
        s for s in historico
        if s.get("setor", "").strip().lower() == setor.lower() and atendente_preenchido(s)
    ]
    historico = historico[::-1][:10]

    for s in historico:
        st.write(f"🟢 **{s.get('senha', '—')}** às {s.get('hora', '—')} por 👤 {s.get('atendente', '—')}")
except Exception as e:
    st.warning(f"⚠️ Não foi possível carregar o histórico. Erro: {e}")
