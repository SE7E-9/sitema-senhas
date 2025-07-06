# Buscar senhas pendentes
try:
    res = requests.get(api_pendentes)
    res.raise_for_status()
    todas = res.json()
    senhas_do_setor = [s for s in todas if s.get("setor", "").strip().lower() == setor.strip().lower()]
except Exception as e:
    st.error(f"Erro ao carregar senhas pendentes: {e}")
    senhas_do_setor = []

# Exibir senhas pendentes
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
                st.error(f"Erro ao atender a senha: {e}")
