from fastapi.testclient import TestClient

from backend.main import app


def test_api_rejeita_descricao_curta():
    """
    VALIDAÇÃO: testa a regra de tamanho no back-end.

    Isso demonstra que a API também valida os dados, mesmo que uma
    solicitação tente ignorar as verificações feitas na interface.
    """

    with TestClient(app) as cliente:
        resposta = cliente.post(
            "/relatos/analisar",
            json={
                "descricao": "curta",
                "bairro": "Centro",
            },
        )

    assert resposta.status_code == 422


def test_health_da_api():
    """VALIDAÇÃO: verifica se o endpoint de saúde da API responde."""

    with TestClient(app) as cliente:
        resposta = cliente.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"