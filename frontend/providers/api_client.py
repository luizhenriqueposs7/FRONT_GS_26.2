import os

import requests
import streamlit as st


class APIError(Exception):
    """Falha traduzida para uma mensagem compreensível ao cidadão."""


@st.cache_resource
def _sessao_http():
    return requests.Session()


def _url_base() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def _tratar_resposta(resposta: requests.Response):
    if resposta.ok:
        try:
            dados = resposta.json()
        except ValueError as erro:
            raise APIError("O serviço devolveu uma resposta incompleta. Tente novamente.") from erro
        if not isinstance(dados, (dict, list)):
            raise APIError("O serviço devolveu uma resposta incompleta. Tente novamente.")
        return dados

    mensagens = {
        401: "A chave de gestor está incorreta ou não foi autorizada.",
        404: "O relato não foi encontrado.",
        422: "Confira a descrição, o bairro e os demais campos antes de enviar.",
        429: "O serviço está recebendo muitas solicitações. Aguarde e tente novamente.",
        502: "A análise de IA falhou. Tente novamente mais tarde.",
        503: "O serviço solicitado ainda não está configurado. Avise o responsável.",
    }
    raise APIError(mensagens.get(resposta.status_code,
                                "Não foi possível concluir a solicitação. Tente novamente."))


def _validar_relatos(dados) -> list[dict]:
    campos = (
        "id", "cidadao_id", "descricao", "bairro", "categoria", "prioridade",
        "resumo", "status", "observacao_gestor", "criado_em", "atualizado_em",
    )
    if not isinstance(dados, list) or any(
        not isinstance(relato, dict)
        or any(not isinstance(relato.get(campo), str) for campo in campos)
        or relato["categoria"] not in ("Buraco", "Iluminação", "Calçada", "Outro")
        or relato["prioridade"] not in ("Baixa", "Média", "Alta")
        or relato["status"] not in (
            "Recebido", "Em análise", "Encaminhado", "Em atendimento",
            "Concluído", "Não confirmado",
        )
        for relato in dados
    ):
        raise APIError("O serviço devolveu uma resposta incompleta. Tente novamente.")
    return dados


def _requisitar(metodo: str, caminho: str, *, timeout=15, **kwargs):
    try:
        resposta = _sessao_http().request(
            metodo, f"{_url_base()}{caminho}", timeout=timeout, **kwargs,
        )
    except requests.Timeout as erro:
        raise APIError("A resposta demorou mais que o esperado. Tente novamente.") from erro
    except requests.RequestException as erro:
        raise APIError("Não foi possível conectar ao serviço. Tente novamente.") from erro
    return _tratar_resposta(resposta)


def analisar_relato(descricao: str, bairro: str) -> dict:
    return _requisitar("POST", "/relatos/analisar", timeout=30,
                       json={"descricao": descricao, "bairro": bairro})


def criar_relato(dados: dict) -> dict:
    relato = _requisitar("POST", "/relatos", json=dados)
    listar_meus_relatos.clear(dados["cidadao_id"])
    listar_relatos_gestor.clear()
    return relato


@st.cache_data(ttl=30, show_spinner=False)
def listar_meus_relatos(cidadao_id: str) -> list[dict]:
    # O identificador faz parte da chave do cache: históricos não se misturam.
    return _validar_relatos(_requisitar("GET", f"/relatos/me/{cidadao_id}"))


@st.cache_data(ttl=30, show_spinner=False)
def listar_relatos_gestor(chave: str) -> list[dict]:
    return _validar_relatos(_requisitar("GET", "/gestor/relatos", headers={"X-Manager-Key": chave}))


def atualizar_status(relato_id: str, status: str, observacao: str, chave: str) -> dict:
    relato = _requisitar("PATCH", f"/gestor/relatos/{relato_id}",
                         headers={"X-Manager-Key": chave},
                         json={"status": status, "observacao_gestor": observacao})
    listar_relatos_gestor.clear(chave)
    listar_meus_relatos.clear(relato["cidadao_id"])
    return relato
