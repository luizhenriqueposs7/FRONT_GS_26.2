from backend.pipelines.classificacao import _classificacao_demonstracao


def test_relato_de_buraco_recebe_categoria_buraco():
    """
    VALIDAÇÃO: verifica se um texto conhecido recebe a categoria esperada.

    No vídeo, mostre que este teste verifica uma regra específica do modo
    demonstrativo; ele não mede a precisão de um LLM.
    """

    resultado = _classificacao_demonstracao(
        "Há um buraco grande no asfalto perto da praça."
    )

    assert resultado.categoria_sugerida == "Buraco"
    assert resultado.fonte_analise == "demonstracao"


def test_relato_de_iluminacao_com_risco_recebe_prioridade_alta():
    """VALIDAÇÃO: confere categoria e prioridade em um exemplo de teste."""

    resultado = _classificacao_demonstracao(
        "Poste apagado e fio exposto na calçada."
    )

    assert resultado.categoria_sugerida == "Iluminação"
    assert resultado.prioridade_sugerida == "Alta"


def test_relato_de_calcada_recebe_categoria_calcada():
    """VALIDAÇÃO: verifica a categoria sugerida para relato sobre calçada."""

    resultado = _classificacao_demonstracao(
        "A calçada está quebrada e dificulta a passagem."
    )

    assert resultado.categoria_sugerida == "Calçada"