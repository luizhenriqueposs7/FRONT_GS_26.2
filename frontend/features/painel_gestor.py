import pandas as pd
import plotly.express as px
import streamlit as st

from frontend.providers import api_client
from frontend.providers.api_client import APIError
from frontend.ui.components import mostrar_prioridade


STATUS_DISPONIVEIS = [
    "Recebido",
    "Em análise",
    "Encaminhado",
    "Em atendimento",
    "Concluído",
    "Não confirmado",
]


def renderizar(chave_gestor: str):
    st.header("Painel da gestão")

    if st.button("Atualizar painel"):
        api_client.listar_relatos_gestor.clear(chave_gestor)

    try:
        # A API confere a chave antes de devolver os relatos da gestão.
        with st.spinner("Carregando o painel..."):
            st.session_state.historico_gestor = api_client.listar_relatos_gestor(chave_gestor)
        relatos = st.session_state.historico_gestor
    except APIError as erro:
        st.error(str(erro))
        return
    except Exception:
        st.error("Não foi possível carregar o painel da gestão.")
        return

    if not relatos:
        st.info("Ainda não existem relatos para analisar.")
        return

    # DataFrame facilita filtrar e agrupar os relatos para a visualização.
    df = pd.DataFrame(relatos)

    # Dois filtros interativos alteram os dados mostrados na tela e no gráfico.
    col_categoria, col_status = st.columns(2)

    categorias = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
    status = ["Todos"] + sorted(df["status"].dropna().unique().tolist())

    filtro_categoria = col_categoria.selectbox(
        "Filtrar por categoria",
        categorias,
    )
    filtro_status = col_status.selectbox(
        "Filtrar por status",
        status,
    )

    filtrado = df.copy()

    if filtro_categoria != "Todas":
        filtrado = filtrado[filtrado["categoria"] == filtro_categoria]

    if filtro_status != "Todos":
        filtrado = filtrado[filtrado["status"] == filtro_status]

    st.caption(f"{len(filtrado)} relato(s) correspondem aos filtros.")

    if filtrado.empty:
        st.info("Nenhum relato corresponde aos filtros selecionados.")
        return

    # Agrupa os relatos para calcular quantos existem por categoria.
    contagem = (
        filtrado.groupby("categoria", as_index=False)
        .size()
        .rename(columns={"size": "Quantidade"})
    )

    # Plotly cria uma visualização interativa com recursos de hover e zoom.
    figura = px.bar(
        contagem,
        x="categoria",
        y="Quantidade",
        color="categoria",
        title="Relatos por categoria",
        labels={"categoria": "Categoria"},
    )
    figura.update_layout(showlegend=False)
    st.plotly_chart(figura)

    st.subheader("Relatos para análise")

    # Cada relato pode ser aberto individualmente para revisão e atualização.
    for relato in filtrado.to_dict(orient="records"):
        with st.expander(
            f"{relato['categoria']} · {relato['bairro']} · "
            f"{relato['status']} · {relato['id'][:8]}"
        ):
            st.write(f"**Descrição original:** {relato['descricao']}")
            st.write(f"**Resumo:** {relato['resumo']}")
            mostrar_prioridade(relato["prioridade"])

            novo_status = st.selectbox(
                "Atualizar status",
                STATUS_DISPONIVEIS,
                index=STATUS_DISPONIVEIS.index(relato["status"]),
                key=f"status_{relato['id']}",
            )
            observacao = st.text_input(
                "Observação para o cidadão",
                value=relato.get("observacao_gestor", ""),
                max_chars=500,
                key=f"observacao_{relato['id']}",
            )

            if st.button(
                "Salvar atualização",
                key=f"salvar_{relato['id']}",
            ):
                try:
                    # A alteração passa pela API, que valida a chave do gestor.
                    api_client.atualizar_status(
                        relato_id=relato["id"],
                        status=novo_status,
                        observacao=observacao,
                        chave=chave_gestor,
                    )
                    st.success("Atualização registrada.")
                    st.rerun()
                except APIError as erro:
                    st.error(str(erro))
                except Exception:
                    st.error("Não foi possível salvar a atualização.")
