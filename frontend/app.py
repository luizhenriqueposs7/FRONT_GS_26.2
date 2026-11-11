import streamlit as st

from frontend.features import (
    minhas_solicitacoes,
    novo_relato,
    painel_gestor,
)
from frontend.state.session import inicializar_estado
from frontend.ui.components import aplicar_estilo_acessivel


# Configura o título, ícone e largura antes de desenhar os componentes.
st.set_page_config(
    page_title="ZelaBairro",
    page_icon="🏙️",
    layout="wide",
)

# Prepara os valores que precisam persistir entre reruns.
inicializar_estado()

st.title("🏙️ ZelaBairro")
st.caption("A cidade melhora quando cada problema encontra seu caminho.")

# Controle de acessibilidade disponível na barra lateral.
alto_contraste = st.sidebar.toggle(
    "Alto contraste",
    value=False,
)
aplicar_estilo_acessivel(alto_contraste)

st.sidebar.header("Navegação")

# Se ativado, abre a interface demonstrativa da gestão.
modo_gestor = st.sidebar.toggle(
    "Modo demonstração da gestão",
    value=False,
)

if modo_gestor:
    # Para esta POC, a chave é pedida na interface e enviada à API.
    # Não é um sistema completo de autenticação de produção.
    chave_gestor = st.sidebar.text_input(
        "Chave de gestor da demonstração",
        type="password",
    )

    if not chave_gestor:
        st.info("Informe a chave de demonstração para abrir o painel.")
    else:
        painel_gestor.renderizar(chave_gestor)
else:
    # A navegação separa o fluxo de registro do acompanhamento dos relatos.
    pagina = st.sidebar.radio(
        "Escolha uma tela",
        ["Registrar um problema", "Minhas solicitações"],
    )

    if pagina == "Registrar um problema":
        novo_relato.renderizar()
    else:
        minhas_solicitacoes.renderizar()

st.sidebar.divider()
st.sidebar.caption(
    "As sugestões automatizadas podem conter erros. "
    "Revise a classificação antes de enviar."
)