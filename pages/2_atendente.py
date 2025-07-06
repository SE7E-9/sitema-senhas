import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Painel do Atendente", layout="centered")
st.title("📋 Painel do Atendente")

# Atualização automática a cada 10 segundos
st_autorefresh(interval=10_000, key="refresh")

# APIs atualizadas para as planilhas do Sheet.best
api_pendentes = "https://api.sheetbest.com/sheets/4967f136-9e15-47ff-b66d-b72b79bcf2d3"  # pendentes
api_atendidas = "https://api.sheetbest.com/sheets/85deb476-3818-459c-9208-e0f41516d286"  # atendidas

# Setores e atendentes configurados
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes_por_setor = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Financeiro A', 'Financeiro B', 'Financeiro C'],
    'Protocolo': ['Protocolo A', 'Protocolo B'],
    'Geral': ['Geral Único']
}

# Seleção de setor e atendente
setor = st.selectbox("Selecione o setor:", setores)
atendente = st.selectbox("Selecione seu nome:", atendentes_por_setor[setor])

# Carregar senhas pendentes
try:
    res = requests.get(api_pendentes)
    res.raise_for_status()
    todas = res.json()
except Exception as e:
    st.error(f"Erro ao carregar senhas pendentes: {e}")
    todas = []

# Filtrar senhas pendentes do setor
senhas_do_setor = [
    s for s in todas
    if s.get("setor", "").strip().lower() == setor.lower()
]

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
                r1 = requests.post(api_atendidas, json=payload)
                r1.raise_for_status()

                r2 = requests.delete(f"{api_pendentes}?id={senha['id']}")
                r2.raise_for_status()

                st.success(f"✅ Senha {senha['senha']} atendida por {atendente}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao registrar atendimento: {e}")

# Função segura para checar se atendente está preenchido
def atendente_preenchido(senha):
    atendente_valor = senha.get("atendente")
    return isinstance(atendente_valor, str) and atendente_valor.strip() != ""

# Mostrar histórico dos últimos atendimentos válidos
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
