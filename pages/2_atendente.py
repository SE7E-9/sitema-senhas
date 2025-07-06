import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Painel do Atendente", layout="centered")
st.title("📋 Painel do Atendente")

# Atualiza automaticamente a cada 10 segundos para pegar senhas novas
st_autorefresh(interval=10_000, key="refresh")

# APIs das planilhas (confirme que estão certas)
api_pendentes = "https://api.sheetbest.com/sheets/f2bab54d-e790-46ea-9371-bd68e68bbcbc"  # Senhas pendentes
api_atendidas = "https://api.sheetbest.com/sheets/bb970f05-0342-4667-8fd4-8c16998c7422"  # Senhas atendidas

# Setores e atendentes (ajuste nomes conforme sua equipe)
setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Financeiro A', 'Financeiro B', 'Financeiro C'],
    'Protocolo': ['Protocolo A', 'Protocolo B'],
    'Geral': ['Geral Único']
}

setor = st.selectbox("Selecione o setor:", setores)
atendente = st.selectbox("Selecione seu nome:", atendentes[setor])

try:
    res = requests.get(api_pendentes)
    res.raise_for_status()
    todas_senhas = res.json()
except Exception as e:
    st.error(f"Erro ao carregar senhas pendentes: {e}")
    todas_senhas = []

# Filtra senhas do setor selecionado
senhas_do_setor = [s for s in todas_senhas if s.get("setor", "").strip().lower() == setor.lower()]

st.subheader(f"🎟️ Senhas Pendentes - {setor}")

if not senhas_do_setor:
    st.info("Nenhuma senha pendente no momento.")
else:
    for senha in senhas_do_setor:
        if "id" not in senha or not senha["id"]:
            continue
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.markdown(f"**{senha.get('senha', '—')}**")
        col2.markdown(f"{senha.get('hora', '—')}")
        if col3.button("Atender", key=senha["id"]):
            # Monta payload para mover senha para atendidas
            payload = {
                "id": senha["id"],
                "senha": senha["senha"],
                "setor": senha["setor"],
                "hora": senha["hora"],
                "atendente": atendente
            }
            try:
                # Salva na planilha de atendidas
                r1 = requests.post(api_atendidas, json=payload)
                r1.raise_for_status()
                # Remove da planilha de pendentes
                r2 = requests.delete(f"{api_pendentes}?id={senha['id']}")
                r2.raise_for_status()
                st.success(f"✅ Senha {senha['senha']} atendida por {atendente}")
                st.experimental_rerun()  # Atualiza a página
            except Exception as e:
                st.error(f"Erro ao atender a senha: {e}")

# Mostrar histórico de últimas 10 senhas atendidas do setor
st.markdown("---")
st.subheader("📚 Últimos Atendimentos")

try:
    res = requests.get(api_atendidas)
    res.raise_for_status()
    historico = [s for s in res.json() if s.get("setor", "").strip().lower() == setor.lower()]
    historico = historico[::-1][:10]
    for s in historico:
        st.write(f"🟢 **{s.get('senha', '—')}** às {s.get('hora', '—')} por 👤 {s.get('atendente', '—')}")
except Exception:
    st.warning("⚠️ Não foi possível carregar o histórico.")
