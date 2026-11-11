from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Literal restringe os valores aceitos pela API.
# Por exemplo, uma categoria diferente das listadas será rejeitada.
Categoria = Literal["Buraco", "Iluminação", "Calçada", "Outro"]
Prioridade = Literal["Baixa", "Média", "Alta"]
Status = Literal[
    "Recebido",
    "Em análise",
    "Encaminhado",
    "Em atendimento",
    "Concluído",
    "Não confirmado",
]


class AnaliseRequest(BaseModel):
    """Dados que o front-end envia para pedir uma análise do relato."""

    model_config = ConfigDict(str_strip_whitespace=True)

    # Field valida tamanho mínimo e máximo no back-end.
    descricao: str = Field(min_length=10, max_length=1500)
    bairro: str = Field(min_length=2, max_length=100)


class AnaliseResponse(BaseModel):
    """Formato estruturado que a análise deve devolver à interface."""

    model_config = ConfigDict(str_strip_whitespace=True)

    categoria_sugerida: Categoria
    prioridade_sugerida: Prioridade
    resumo: str = Field(min_length=5, max_length=300)
    justificativa: str = Field(min_length=5, max_length=500)

    # Indica se a resposta veio de um LLM configurado ou do modo demonstrativo.
    fonte_analise: Literal["llm", "demonstracao"]


class CriarRelatoRequest(BaseModel):
    """Dados que são persistidos depois que o cidadão confirma o envio."""

    model_config = ConfigDict(str_strip_whitespace=True)

    cidadao_id: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=10, max_length=1500)
    bairro: str = Field(min_length=2, max_length=100)
    categoria: Categoria
    prioridade: Prioridade
    resumo: str = Field(min_length=5, max_length=300)


class AtualizarRelatoRequest(BaseModel):
    """Dados que o gestor envia ao atualizar uma solicitação."""

    model_config = ConfigDict(str_strip_whitespace=True)

    status: Status
    observacao_gestor: str = Field(default="", max_length=500)


class RelatoResponse(BaseModel):
    """Estrutura padrão dos relatos devolvidos pela API."""

    id: str
    cidadao_id: str
    descricao: str
    bairro: str
    categoria: Categoria
    prioridade: Prioridade
    resumo: str
    status: Status
    observacao_gestor: str
    criado_em: datetime
    atualizado_em: datetime
