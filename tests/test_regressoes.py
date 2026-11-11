import json

import httpx
import pytest


ENTRADA = {"descricao": "Há um buraco grande no asfalto perto da praça.", "bairro": "Centro"}
REGISTRO = {
    **ENTRADA, "cidadao_id": "cidadao-teste", "categoria": "Buraco",
    "prioridade": "Média", "resumo": "Buraco no asfalto perto da praça.",
}


@pytest.mark.parametrize("campo,valor", [("descricao", " " * 10), ("bairro", "  ")])
def test_analise_rejeita_entrada_sem_conteudo(cliente, campo, valor):
    assert cliente.post("/relatos/analisar", json={**ENTRADA, campo: valor}).status_code == 422


@pytest.mark.parametrize("campo,valor", [("descricao", " " * 10), ("bairro", "  "), ("resumo", " " * 5)])
def test_criacao_rejeita_entrada_sem_conteudo(cliente, campo, valor):
    assert cliente.post("/relatos", json={**REGISTRO, campo: valor}).status_code == 422
    assert cliente.get("/relatos/me/cidadao-teste").json() == []


def test_criacao_remove_espacos_externos(cliente):
    result = cliente.post("/relatos", json={**REGISTRO, "bairro": " Centro "})
    assert result.status_code == 200
    assert result.json()["bairro"] == "Centro"


def test_sem_llm_nao_substitui_ia_por_regras(cliente, monkeypatch):
    monkeypatch.delenv("DEMO_MODE", raising=False)
    assert cliente.post("/relatos/analisar", json=ENTRADA).status_code == 503


def test_demonstracao_precisa_ser_explicita(cliente):
    result = cliente.post("/relatos/analisar", json=ENTRADA)
    assert result.status_code == 200
    assert result.json()["fonte_analise"] == "demonstracao"


@pytest.mark.parametrize("tipo", ["valido", "json_invalido", "categoria_invalida", "timeout"])
def test_contrato_real_do_adaptador_llm(cliente, monkeypatch, tipo):
    monkeypatch.setenv("DEMO_MODE", "false")
    monkeypatch.setenv("LLM_BASE_URL", "https://provedor.invalid/v1")
    monkeypatch.setenv("LLM_API_KEY", "credencial-sintetica")
    monkeypatch.setenv("LLM_MODEL", "modelo-de-teste")
    analysis = {
        "categoria_sugerida": "Buraco" if tipo != "categoria_invalida" else "Inexistente",
        "prioridade_sugerida": "Média", "resumo": "Buraco no asfalto perto da praça.",
        "justificativa": "O relato descreve uma falha na pavimentação.",
    }

    def transporte(url, **kwargs):
        assert url == "https://provedor.invalid/v1/chat/completions"
        assert kwargs["json"]["model"] == "modelo-de-teste"
        assert kwargs["headers"]["Authorization"] == "Bearer credencial-sintetica"
        if tipo == "timeout":
            raise httpx.ReadTimeout("timeout sintético")
        content = "isto não é JSON" if tipo == "json_invalido" else json.dumps(analysis)
        return httpx.Response(200, request=httpx.Request("POST", url), json={
            "choices": [{"message": {"content": content}}],
        })

    monkeypatch.setattr("backend.providers.llm.httpx.post", transporte)
    result = cliente.post("/relatos/analisar", json=ENTRADA)
    if tipo == "valido":
        assert result.status_code == 200
        assert result.json()["categoria_sugerida"] == "Buraco"
        assert result.json()["fonte_analise"] == "llm"
    else:
        assert result.status_code == 502
        assert "Traceback" not in result.text


def test_gestao_protegida_e_historicos_separados(cliente):
    created = cliente.post("/relatos", json=REGISTRO).json()
    assert cliente.get("/gestor/relatos").status_code == 401
    assert cliente.get("/relatos/me/outro-cidadao").json() == []
    headers = {"X-Manager-Key": "chave-exclusiva-dos-testes"}
    result = cliente.patch(f"/gestor/relatos/{created['id']}", headers=headers,
                           json={"status": "Concluído", "observacao_gestor": "Atendimento de teste."})
    assert result.status_code == 200
    history = cliente.get("/relatos/me/cidadao-teste").json()
    assert history[0]["status"] == "Concluído"


def test_cors_restringe_origem(cliente):
    headers = {"Origin": "https://origem-nao-autorizada.invalid", "Access-Control-Request-Method": "POST"}
    assert cliente.options("/relatos", headers=headers).status_code == 400
