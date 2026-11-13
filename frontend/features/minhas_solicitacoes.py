import streamlit as st

from frontend.providers import api_client
from frontend.providers.api_client import APIError
from frontend.ui.components import DESCRICOES_STATUS, mostrar_cartao_relato


def renderizar():
    st.header("Minhas solicitações")
    st.write("Acompanhe os relatos enviados nesta sessão pelo número de acompanhamento (protocolo).")
    st.caption("Os status são atualizações desta demonstração e não abrem atendimento municipal automaticamente.")
    with st.expander("O que significa cada status?"):
        for status, explicacao in DESCRICOES_STATUS.items():
            st.markdown(f"**{status}:** {explicacao}")

    if st.button("Atualizar solicitações"):
        api_client.listar_meus_relatos.clear(st.session_state.cidadao_id)
        st.session_state.historico_carregado = False

    try:
        if not st.session_state.historico_carregado:
            with st.spinner("Carregando suas solicitações..."):
                st.session_state.historico = api_client.listar_meus_relatos(st.session_state.cidadao_id)
            st.session_state.historico_carregado = True
        relatos = st.session_state.historico
    except APIError as erro:
        st.error(str(erro))
        return
    except Exception:
        st.error("Não foi possível carregar suas solicitações.")
        return

    # Estado vazio: explica ao cidadão o que fazer quando não há registros.
    if not relatos:
        st.info(
            "Ainda não há solicitações nesta sessão. "
            "Use a tela Registrar um problema para começar."
        )
        return

    # Reutiliza o mesmo componente para cada item da lista.
    st.caption("Use Atualizar solicitações para buscar mudanças feitas pela gestão.")
    for relato in relatos:
        mostrar_cartao_relato(relato)
