import os

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.providers import repository


@pytest.fixture(autouse=True)
def ambiente_isolado(monkeypatch, tmp_path):
    monkeypatch.setattr(repository, "DATABASE_PATH", str(tmp_path / "relatos.db"))
    for key in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setenv("MANAGER_API_KEY", "chave-exclusiva-dos-testes")


@pytest.fixture
def cliente():
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client
