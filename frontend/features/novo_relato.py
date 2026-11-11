import streamlit as st

from frontend.providers import api_client
from frontend.providers.api_client import APIError
from frontend.state.session import guardar_analise, limpar_analise_pendente, registrar_no_historico
from frontend.ui.components import mostrar_prioridade


CATEGORIAS = ["Buraco", "Iluminação", "Calçada", "Outro"]
PRIORIDADES = ["Baixa", "Média", "Alta"]


def renderizar():
    st.header("Registrar um problema")
    st.write(
        "Descreva o que está acontecendo. A análise é uma sugestão "
        "e você poderá revisá-la antes do envio."
    )

    if st.session_state.ultimo_relato:
        st.success("Relato registrado.")
        st.write(f"**Seu protocolo:** `{st.session_state.ultimo_relato['id']}`")
        st.write("Você pode acompanhar o status em Minhas solicitações.")

    # O formulário agrupa a entrada e evita o envio a cada alteração de campo.
    with st.form("formulario_relato"):
        bairro = st.text_input(
            "Bairro ou região",
            max_chars=100,
            help="Não informe seu endereço residencial.",
        )
        descricao = st.text_area(
            "O que aconteceu?",
            max_chars=1500,
            height=160,
            help="Descreva o problema e um ponto de referência público.",
        )
        enviar_analise = st.form_submit_button("Analisar relato")

    if enviar_analise:
        limpar_analise_pendente()
        st.session_state.ultimo_relato = None
        # VALIDAÇÃO no front-end: dá retorno imediato ao cidadão.
        # O back-end também valida os dados; a interface não é a única barreira.
        if len(bairro.strip()) < 2:
            st.error("Informe o bairro ou a região.")
            return

        if len(descricao.strip()) < 10:
            st.error("Descreva o problema com pelo menos 10 caracteres.")
            return

        try:
            # O spinner comunica que o sistema está trabalhando.
            with st.spinner("Analisando o relato..."):
                analise = api_client.analisar_relato(
                    descricao=descricao.strip(),
                    bairro=bairro.strip(),
                )

            guardar_analise(bairro.strip(), descricao.strip(), analise)

        except APIError as erro:
            st.error(str(erro))
        except Exception:
            # Evita expor detalhes técnicos ao cidadão.
            st.error("Não foi possível conectar ao serviço. Tente novamente.")

    pendente = st.session_state.get("analise_pendente")
    if not pendente:
        return

    st.divider()
    st.subheader("Revise a sugestão da IA")
    analise = pendente["analise"]

    # Identifica claramente quando o resultado veio das regras demonstrativas.
    if analise["fonte_analise"] == "demonstracao":
        st.info(
            "Modo demonstração: esta classificação usa regras simples, "
            "não um modelo de IA conectado."
        )

    st.write(f"**Resumo sugerido:** {analise['resumo']}")
    st.write(f"**Por que foi sugerido:** {analise['justificativa']}")
    mostrar_prioridade(analise["prioridade_sugerida"])

    # HUMAN-IN-THE-LOOP: o cidadão pode confirmar ou corrigir a sugestão.
    categoria = st.selectbox(
        "Categoria — confirme ou corrija",
        CATEGORIAS,
        index=CATEGORIAS.index(analise["categoria_sugerida"]),
        key=f"categoria_{pendente['id']}",
    )
    prioridade = st.selectbox(
        "Prioridade sugerida — confirme ou corrija",
        PRIORIDADES,
        index=PRIORIDADES.index(analise["prioridade_sugerida"]),
        key=f"prioridade_{pendente['id']}",
    )

    confirmar = st.checkbox(
        "Revisei os dados e quero enviar este relato.",
        key=f"confirmar_{pendente['id']}",
    )

    if st.button("Enviar relato", type="primary"):
        if not confirmar:
            st.warning("Marque a confirmação antes de enviar.")
            return

        dados = {
            "cidadao_id": st.session_state.cidadao_id,
            "descricao": pendente["descricao"],
            "bairro": pendente["bairro"],
            "categoria": categoria,
            "prioridade": prioridade,
            "resumo": analise["resumo"],
        }

        try:
            with st.spinner("Registrando o relato..."):
                relato = api_client.criar_relato(dados)
            registrar_no_historico(relato)
            st.rerun()

        except APIError as erro:
            st.error(str(erro))
        except Exception:
            st.error("Não foi possível enviar o relato. Tente novamente.")
