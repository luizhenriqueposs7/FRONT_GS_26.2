import os

from backend.providers.llm import analisar_com_llm
from backend.schemas.relato import AnaliseResponse


def _classificacao_demonstracao(descricao: str) -> AnaliseResponse:
    """
    Classificação simples para testar a aplicação sem credenciais de LLM.

    VÍDEO: explique que este modo usa regras e palavras-chave; ele não
    representa um modelo de IA conectado nem uma avaliação de precisão.
    """

    texto = descricao.lower()

    # Procura termos relacionados a cada tipo de ocorrência.
    if any(palavra in texto for palavra in ["buraco", "cratera", "asfalto"]):
        categoria = "Buraco"
    elif any(
        palavra in texto
        for palavra in ["poste", "luz", "iluminação", "iluminacao", "escuro"]
    ):
        categoria = "Iluminação"
    elif any(
        palavra in texto
        for palavra in ["calçada", "calcada", "piso", "rampa"]
    ):
        categoria = "Calçada"
    else:
        categoria = "Outro"

    # A prioridade é apenas uma sugestão demonstrativa.
    palavras_urgentes = [
        "acidente",
        "queda",
        "fio exposto",
        "sem luz",
        "risco",
        "perigo",
    ]
    prioridade = (
        "Alta"
        if any(palavra in texto for palavra in palavras_urgentes)
        else "Média"
    )

    # Limita o resumo para caber no campo definido no schema.
    resumo = descricao.strip()
    if len(resumo) > 250:
        resumo = resumo[:247].rstrip() + "..."

    return AnaliseResponse(
        categoria_sugerida=categoria,
        prioridade_sugerida=prioridade,
        resumo=resumo,
        justificativa=(
            "Classificação demonstrativa baseada em palavras do relato. "
            "Revise antes de enviar."
        ),
        fonte_analise="demonstracao",
    )


def analisar_relato(descricao: str, bairro: str) -> AnaliseResponse:
    """Escolhe entre o LLM configurado e a demonstração local."""

    if os.getenv("DEMO_MODE", "false").strip().lower() == "true":
        return _classificacao_demonstracao(descricao)
    return analisar_com_llm(descricao, bairro)
