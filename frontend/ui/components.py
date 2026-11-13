import streamlit as st


DESCRICOES_STATUS = {
    "Recebido": "Seu relato foi salvo e aguarda a revisão da gestão.",
    "Em análise": "A equipe está avaliando as informações do relato.",
    "Encaminhado": "A gestão direcionou o relato para a próxima etapa de avaliação.",
    "Em atendimento": "A gestão marcou uma ação de acompanhamento em andamento.",
    "Concluído": "A gestão encerrou o acompanhamento. Confira a observação do relato.",
    "Não confirmado": "As informações disponíveis não foram suficientes para confirmar o relato.",
}


def aplicar_estilo_acessivel(alto_contraste: bool):
    """Aplica o tema de alto contraste quando o controle está ativado."""

    if alto_contraste:
        st.markdown(
            """
            <style>
            .stApp {
                background: #000000;
                color: #ffffff;
            }
            [data-testid="stWidgetLabel"] {
                color: #ffffff !important;
            }
            .stButton button {
                border: 2px solid #ffffff;
                font-weight: 700;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def mostrar_status(status: str):
    """
    Apresenta o status com texto e ícone.

    A informação não depende somente da cor, o que ajuda na acessibilidade.
    """

    icones = {
        "Recebido": "📥",
        "Em análise": "🔎",
        "Encaminhado": "➡️",
        "Em atendimento": "🛠️",
        "Concluído": "✅",
        "Não confirmado": "ℹ️",
    }
    st.write(f"{icones.get(status, '•')} **{status}**")
    st.caption(DESCRICOES_STATUS.get(status, "Consulte a observação da gestão para mais informações."))


def mostrar_prioridade(prioridade: str):
    cores = {"Alta": ("red", "⚠️"), "Média": ("orange", "●"), "Baixa": ("blue", "ℹ️")}
    cor, icone = cores[prioridade]
    st.markdown(f":{cor}[{icone} **Prioridade sugerida: {prioridade}**]")


def mostrar_cartao_relato(relato: dict):
    """Apresenta um relato com status, prioridade e protocolo."""

    with st.container(border=True):
        st.subheader(f"{relato['categoria']} — {relato['bairro']}")
        mostrar_status(relato["status"])
        mostrar_prioridade(relato["prioridade"])
        st.write(relato["resumo"])
        st.caption("Número de acompanhamento (protocolo)")
        st.code(relato["id"], language=None)

        if relato.get("observacao_gestor"):
            st.info(f"Atualização da gestão: {relato['observacao_gestor']}")
