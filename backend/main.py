import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.providers.repository import inicializar_banco
from backend.routers.relatos import router as relatos_router


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    inicializar_banco()
    yield


app = FastAPI(
    title="ZelaBairro API",
    version="1.0.0",
    description="API demonstrativa para zeladoria urbana colaborativa.",
    lifespan=ciclo_de_vida,
)

# CORS controla quais endereços podem acessar a API pelo navegador.
# Em produção, configure somente as origens realmente utilizadas.
origens = [
    origem.strip()
    for origem in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8501",
    ).split(",")
    if origem.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "X-Manager-Key"],
)

# Registra neste aplicativo as rotas definidas no módulo de relatos.
app.include_router(relatos_router)


@app.get("/health")
def health():
    """Endpoint simples para conferir se a API está ativa."""

    modo = "llm" if all(os.getenv(key, "").strip() for key in
                        ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL")) else "nao_configurado"
    if os.getenv("DEMO_MODE", "false").strip().lower() == "true":
        modo = "demonstracao"
    return {"status": "ok", "servico": "zelabairro-api", "modo_analise": modo,
            "modelo": os.getenv("LLM_MODEL", "") if modo == "llm" else None}
