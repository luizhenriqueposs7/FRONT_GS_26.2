import json
from urllib.parse import urlsplit

import pytest
import requests
import streamlit as st

from frontend.providers import api_client


@pytest.fixture(autouse=True)
def limpar_caches():
    st.cache_data.clear()
    st.cache_resource.clear()
    yield
    st.cache_data.clear()
    st.cache_resource.clear()


def resposta(status, payload):
    response = requests.Response()
    response.status_code = status
    response._content = json.dumps(payload).encode()
    return response


def test_erro_422_nao_expoe_estrutura_tecnica():
    response = resposta(422, {"detail": [{"loc": ["body", "descricao"], "type": "string_too_short", "msg": "String should have at least 10 characters"}]})
    with pytest.raises(api_client.APIError) as caught:
        api_client._tratar_resposta(response)
    message = str(caught.value)
    assert "descrição" in message.lower()
    assert "body" not in message and "string_too_short" not in message


def test_json_invalido_vira_erro_compreensivel():
    response = resposta(200, {})
    response._content = b"<html>indisponivel</html>"
    with pytest.raises(api_client.APIError):
        api_client._tratar_resposta(response)


@pytest.mark.parametrize("exception", [requests.Timeout("segredo"), requests.ConnectionError("host interno")])
def test_falha_de_rede_nao_escapa_do_cliente(monkeypatch, exception):
    def transporte(*args, **kwargs):
        raise exception
    monkeypatch.setattr(requests.Session, "request", transporte)
    with pytest.raises(api_client.APIError) as caught:
        api_client.analisar_relato("Há um buraco na praça.", "Centro")
    assert "segredo" not in str(caught.value)
    assert "host interno" not in str(caught.value)


def test_cache_separa_historicos_e_evitar_consultas_repetidas(monkeypatch):
    calls = []
    def transporte(self, method, url, **kwargs):
        calls.append(url)
        return resposta(200, [{"id": url.rsplit("/", 1)[-1]}])
    monkeypatch.setattr(requests.Session, "request", transporte)
    assert api_client.listar_meus_relatos("cidadao-a") == [{"id": "cidadao-a"}]
    assert api_client.listar_meus_relatos("cidadao-a") == [{"id": "cidadao-a"}]
    assert api_client.listar_meus_relatos("cidadao-b") == [{"id": "cidadao-b"}]
    assert len(calls) == 2


def test_mutacoes_invalidam_historico_e_cache_da_gestao(monkeypatch, cliente):
    def transporte(self, method, url, **kwargs):
        result = cliente.request(method, urlsplit(url).path, json=kwargs.get("json"),
                                 headers=kwargs.get("headers"))
        return resposta(result.status_code, result.json())
    monkeypatch.setattr(requests.Session, "request", transporte)
    assert api_client.listar_meus_relatos("cidadao-a") == []
    record = api_client.criar_relato({
        "cidadao_id": "cidadao-a", "descricao": "Há um buraco na praça.", "bairro": "Centro",
        "categoria": "Buraco", "prioridade": "Média", "resumo": "Buraco na praça.",
    })
    assert len(api_client.listar_meus_relatos("cidadao-a")) == 1
    key = "chave-exclusiva-dos-testes"
    assert api_client.listar_relatos_gestor(key)[0]["status"] == "Recebido"
    with pytest.raises(api_client.APIError):
        api_client.listar_relatos_gestor("chave-nao-autorizada")
    api_client.atualizar_status(record["id"], "Concluído", "Teste de atualização.", key)
    assert api_client.listar_relatos_gestor(key)[0]["status"] == "Concluído"
    assert api_client.listar_meus_relatos("cidadao-a")[0]["status"] == "Concluído"
