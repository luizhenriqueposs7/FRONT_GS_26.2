import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


# Permite alterar o caminho do banco por variável de ambiente.
# Se não houver configuração, usa a pasta data do projeto.
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/zelabairro.db")


def _conectar():
    """Abre uma conexão com o banco SQLite."""

    caminho = Path(DATABASE_PATH)

    # Cria a pasta do banco caso ela ainda não exista.
    caminho.parent.mkdir(parents=True, exist_ok=True)

    # row_factory permite acessar as colunas pelo nome.
    conexao = sqlite3.connect(caminho, check_same_thread=False)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    """Cria a tabela necessária na primeira inicialização."""

    with _conectar() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS relatos (
                id TEXT PRIMARY KEY,
                cidadao_id TEXT NOT NULL,
                descricao TEXT NOT NULL,
                bairro TEXT NOT NULL,
                categoria TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                resumo TEXT NOT NULL,
                status TEXT NOT NULL,
                observacao_gestor TEXT NOT NULL DEFAULT '',
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
            """
        )


def criar_relato(dados: dict) -> dict:
    """Salva um relato confirmado e gera seu protocolo."""

    # O mesmo horário é usado para criação e primeira atualização.
    agora = datetime.now(timezone.utc).isoformat()

    registro = {
        "id": str(uuid4()),  # Identificador único usado como protocolo.
        **dados,
        "status": "Recebido",  # Todo relato começa com este status.
        "observacao_gestor": "",
        "criado_em": agora,
        "atualizado_em": agora,
    }

    with _conectar() as conexao:
        # Os valores são enviados como parâmetros, evitando montar SQL
        # concatenando o conteúdo informado pelo usuário.
        conexao.execute(
            """
            INSERT INTO relatos (
                id, cidadao_id, descricao, bairro, categoria, prioridade,
                resumo, status, observacao_gestor, criado_em, atualizado_em
            ) VALUES (
                :id, :cidadao_id, :descricao, :bairro, :categoria, :prioridade,
                :resumo, :status, :observacao_gestor, :criado_em, :atualizado_em
            )
            """,
            registro,
        )

    return registro


def listar_por_cidadao(cidadao_id: str) -> list[dict]:
    """Retorna os relatos associados ao identificador da sessão."""

    with _conectar() as conexao:
        linhas = conexao.execute(
            """
            SELECT * FROM relatos
            WHERE cidadao_id = ?
            ORDER BY criado_em DESC
            """,
            (cidadao_id,),
        ).fetchall()

    return [dict(linha) for linha in linhas]


def listar_todos() -> list[dict]:
    """Lista todos os relatos para o painel demonstrativo de gestão."""

    with _conectar() as conexao:
        linhas = conexao.execute(
            "SELECT * FROM relatos ORDER BY criado_em DESC"
        ).fetchall()

    return [dict(linha) for linha in linhas]


def atualizar_status(
    relato_id: str,
    status: str,
    observacao_gestor: str,
) -> dict | None:
    """Atualiza status e observação visível ao cidadão."""

    agora = datetime.now(timezone.utc).isoformat()

    with _conectar() as conexao:
        cursor = conexao.execute(
            """
            UPDATE relatos
            SET status = ?, observacao_gestor = ?, atualizado_em = ?
            WHERE id = ?
            """,
            (status, observacao_gestor, agora, relato_id),
        )

        # Se nenhuma linha foi atualizada, o protocolo não existe.
        if cursor.rowcount == 0:
            return None

        linha = conexao.execute(
            "SELECT * FROM relatos WHERE id = ?",
            (relato_id,),
        ).fetchone()

    return dict(linha) if linha else None