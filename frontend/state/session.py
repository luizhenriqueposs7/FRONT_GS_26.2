from uuid import uuid4

import streamlit as st


def inicializar_estado():
    """Inicializa os dados persistentes entre reruns do Streamlit."""

    if "cidadao_id" not in st.session_state:
        # Identificador temporário da sessão, não é uma conta de usuário.
        st.session_state.cidadao_id = str(uuid4())

    if "analise_pendente" not in st.session_state:
        st.session_state.analise_pendente = None

    if "historico" not in st.session_state:
        st.session_state.historico = []
        st.session_state.historico_carregado = False

    if "ultimo_relato" not in st.session_state:
        st.session_state.ultimo_relato = None


def iniciar_nova_analise():
    limpar_analise_pendente()
    st.session_state.ultimo_relato = None


def guardar_analise(bairro: str, descricao: str, analise: dict):
    st.session_state.analise_pendente = {
        "id": str(uuid4()), "bairro": bairro, "descricao": descricao, "analise": analise,
    }


def registrar_no_historico(relato: dict):
    historico = st.session_state.historico
    st.session_state.historico = [relato] + [item for item in historico if item["id"] != relato["id"]]
    st.session_state.ultimo_relato = relato
    limpar_analise_pendente()


def limpar_analise_pendente():
    """Limpa o resultado temporário depois que o relato é enviado."""

    st.session_state.analise_pendente = None
