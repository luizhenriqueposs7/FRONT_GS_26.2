import hmac
import os

from fastapi import APIRouter, Header, HTTPException

from backend.pipelines.classificacao import analisar_relato
from backend.providers import repository
from backend.providers.llm import LLMIndisponivel, LLMNaoConfigurado
from backend.schemas.relato import (
    AnaliseRequest,
    AnaliseResponse,
    AtualizarRelatoRequest,
    CriarRelatoRequest,
    RelatoResponse,
)


router = APIRouter()


def _validar_chave_gestor(chave: str | None):
    """
    Confere a chave compartilhada usada na demonstração.

    IMPORTANTE: isso não é autenticação individual nem RBAC completo
    para um sistema em produção.
    """

    esperada = os.getenv("MANAGER_API_KEY", "").strip()

    if not esperada:
        raise HTTPException(
            status_code=503,
            detail="A área de gestão não está configurada nesta demonstração.",
        )

    # compare_digest evita comparação direta da chave como texto comum.
    if not chave or not hmac.compare_digest(chave, esperada):
        raise HTTPException(
            status_code=401,
            detail="Acesso de gestor não autorizado.",
        )


@router.post("/relatos/analisar", response_model=AnaliseResponse)
def analisar(request: AnaliseRequest):
    """Valida a entrada e devolve a análise estruturada."""

    try:
        return analisar_relato(request.descricao, request.bairro)
    except LLMNaoConfigurado as erro:
        raise HTTPException(status_code=503, detail=str(erro)) from erro
    except LLMIndisponivel as erro:
        # Converte a falha do provedor em erro HTTP compreensível para o cliente.
        raise HTTPException(
            status_code=502,
            detail=str(erro),
        ) from erro


@router.post("/relatos", response_model=RelatoResponse)
def criar(request: CriarRelatoRequest):
    """Registra o relato depois da revisão e confirmação no front-end."""

    return repository.criar_relato(request.model_dump())


@router.get(
    "/relatos/me/{cidadao_id}",
    response_model=list[RelatoResponse],
)
def listar_do_cidadao(cidadao_id: str):
    """Lista os relatos associados ao identificador da sessão."""

    return repository.listar_por_cidadao(cidadao_id)


@router.get(
    "/gestor/relatos",
    response_model=list[RelatoResponse],
)
def listar_para_gestor(
    x_manager_key: str | None = Header(default=None),
):
    """Rota protegida usada pelo painel da gestão."""

    _validar_chave_gestor(x_manager_key)
    return repository.listar_todos()


@router.patch(
    "/gestor/relatos/{relato_id}",
    response_model=RelatoResponse,
)
def atualizar_para_gestor(
    relato_id: str,
    request: AtualizarRelatoRequest,
    x_manager_key: str | None = Header(default=None),
):
    """Atualiza o status depois da análise humana da equipe gestora."""

    _validar_chave_gestor(x_manager_key)

    atualizado = repository.atualizar_status(
        relato_id=relato_id,
        status=request.status,
        observacao_gestor=request.observacao_gestor,
    )

    if atualizado is None:
        raise HTTPException(status_code=404, detail="Relato não encontrado.")

    return atualizado
