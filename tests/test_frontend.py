from pathlib import Path

import requests
from streamlit.testing.v1 import AppTest

from frontend.providers import api_client


APP = Path(__file__).parents[1] / "frontend" / "app.py"
ANALISE = {
    "categoria_sugerida": "Buraco", "prioridade_sugerida": "Média",
    "resumo": "Buraco no asfalto perto da praça.",
    "justificativa": "O relato descreve um buraco na via.", "fonte_analise": "demonstracao",
}


def botao(app, label):
    return next(button for button in app.button if button.label == label)


def analisar(app, descricao="Há um buraco no asfalto da praça."):
    app.text_input[0].set_value("Centro")
    app.text_area[0].set_value(descricao)
    botao(app, "Analisar relato").click().run()
    assert not app.exception


def test_nova_analise_exige_nova_confirmacao(monkeypatch):
    monkeypatch.setattr(api_client, "analisar_relato", lambda **kwargs: dict(ANALISE))
    app = AppTest.from_file(str(APP), default_timeout=20).run()
    analisar(app)
    app.checkbox[0].check().run()
    assert app.checkbox[0].value
    analisar(app, "Há outro buraco no asfalto da rua.")
    assert app.checkbox[0].value is False


def test_falha_na_nova_analise_remove_resultado_antigo(monkeypatch):
    monkeypatch.setattr(api_client, "analisar_relato", lambda **kwargs: dict(ANALISE))
    app = AppTest.from_file(str(APP), default_timeout=20).run()
    analisar(app)
    def falhar(**kwargs):
        raise api_client.APIError("A análise está indisponível. Tente novamente.")
    monkeypatch.setattr(api_client, "analisar_relato", falhar)
    analisar(app, "Outro problema na calçada perto da escola.")
    assert len(app.error) == 1
    assert not app.checkbox
    assert not app.selectbox


def test_relato_confirmado_alimenta_historico_da_sessao(monkeypatch):
    monkeypatch.setattr(api_client, "analisar_relato", lambda **kwargs: dict(ANALISE))
    monkeypatch.setattr(api_client, "criar_relato", lambda data: {
        **data, "id": "protocolo-sintetico", "status": "Recebido", "observacao_gestor": "",
        "criado_em": "2026-11-10T12:00:00+00:00", "atualizado_em": "2026-11-10T12:00:00+00:00",
    })
    app = AppTest.from_file(str(APP), default_timeout=20).run()
    analisar(app)
    app.checkbox[0].check().run()
    botao(app, "Enviar relato").click().run()
    assert not app.exception
    history = app.session_state["historico"]
    assert any(item["id"] == "protocolo-sintetico" for item in history)
    assert app.session_state["analise_pendente"] is None


def test_falha_na_nova_analise_nao_mostra_sucesso_do_relato_anterior(monkeypatch):
    def falhar(**kwargs):
        raise api_client.APIError("Não foi possível conectar ao serviço. Tente novamente.")
    monkeypatch.setattr(api_client, "analisar_relato", falhar)
    app = AppTest.from_file(str(APP), default_timeout=20)
    app.session_state["ultimo_relato"] = {"id": "protocolo-anterior"}
    app.run()
    assert app.success
    analisar(app)
    assert app.error
    assert not app.success
    assert app.session_state["ultimo_relato"] is None


def test_painel_trata_json_fora_do_contrato_sem_expor_excecao(monkeypatch):
    response = requests.Response()
    response.status_code = 200
    response._content = b'{"unexpected":123}'
    monkeypatch.setattr(requests.Session, "request", lambda *args, **kwargs: response)
    api_client.listar_relatos_gestor.clear()
    app = AppTest.from_file(str(APP), default_timeout=20).run()
    app.toggle[1].set_value(True).run()
    app.text_input[0].set_value("chave-sintetica-da-regressao").run()
    assert not app.exception
    assert len(app.error) == 1
    assert "resposta incompleta" in app.error[0].value
