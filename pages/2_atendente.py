import streamlit as st
import requests

st.title("📋 Painel do Atendente")

setores = ['Veículos', 'Financeiro', 'Protocolo', 'Geral']
atendentes_por_setor = {
    'Veículos': ['Atendente 1', 'Atendente 2', 'Atendente 3', 'Atendente 4', 'Atendente 5'],
    'Financeiro': ['Atendente A', 'Atendente B', 'Atendente C'],
    'Protocolo': ['Atendente X', 'Atendente Y'],
    'Geral': ['Atendente Único']
}

api_pendentes = "https://api.sheetbest.com/sheets/f2bab54d-e790-46ea-9371-bd68e68bbcbc"
api_atendidas = "https://api.sheetbest.com/sheets/bb970f05-0342-4667-8fd4-8c16998c7422"

setor = st.selectbox("Selecione seu setor:", setores)
atendente = st.selectbox("Seu nome:", atendentes_por_setor[setor])

# Carregar senhas pendentes
res = requests.get(api_pendentes)
senhas = res.json()
senhas_setor = [s for s in senhas if s["setor"] == setor]

st.subheader(f"Senhas pendentes para o setor {setor}")

if not senhas_setor:
    st.info("Nenhuma senha pendente no momento.")
else:
    for senha in senhas_setor:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{senha['senha']}**")
        col2.write(f"Hora: {senha['hora']}")
        if col3.button("Atender", key=f"btn_{senha['senha']}"):
            # 1. Mover para aba "Atendidas"
            payload = {
                "senha": senha["senha"],
                "setor": senha["setor"],
                "hora": senha["hora"],
                "atendente": atendente
            }
            requests.post(api_atendidas, json=payload)

            # 2. Remover da aba "Pendentes"
            requests.delete(f"{api_pendentes}?senha={senha['senha']}&setor={senha['setor']}&hora={senha['hora']}")
            st.success(f"Senha {senha['senha']} atendida por {atendente}")
            st.experimental_rerun()

st.markdown("---")
st.subheader("Últimas senhas atendidas")

res2 = requests.get(api_atendidas)
atendidas = res2.json()
filtradas = [s for s in atendidas if s["setor"] == setor]

if not filtradas:
    st.info("Nenhuma senha atendida ainda.")
else:
    for item in filtradas[::-1][:10]:
        st.write(f"**{item['senha']}** - {item['hora']} - 👤 {item.get('atendente', '—')}")
