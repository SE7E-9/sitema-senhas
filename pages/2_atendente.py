for senha in senhas_do_setor:
    # Ignora senhas antigas sem ID
    if "id" not in senha or not senha["id"]:
        continue

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
            r = requests.post(api_atendidas, json=payload)
            if r.status_code != 200:
                st.error("Erro ao salvar em atendidas.")
                st.stop()

            r2 = requests.delete(f"{api_pendentes}?id={senha['id']}")
            if r2.status_code == 200:
                st.success(f"Senha {senha['senha']} atendida.")
                st.experimental_rerun()
            else:
                st.error("Erro ao remover da lista.")
        except Exception as e:
            st.error(f"Erro ao atender: {e}")
