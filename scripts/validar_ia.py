"""Coleta três execuções reais da API e atualiza as evidências do README."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx


CASOS = [
    ("Há um buraco grande no asfalto perto da praça.", "Buraco"),
    ("Poste apagado e fio exposto na calçada.", "Iluminação"),
    ("A calçada está quebrada e dificulta a passagem.", "Calçada"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", default="http://localhost:8000")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    now = datetime.now(timezone.utc)
    results = []
    with httpx.Client(base_url=args.api_url.rstrip("/"), timeout=40) as client:
        health = client.get("/health")
        health.raise_for_status()
        health = health.json()
        if health.get("modo_analise") != "llm":
            raise SystemExit("A API precisa estar configurada com LLM real e DEMO_MODE=false.")
        for description, expected in CASOS:
            response = client.post("/relatos/analisar", json={"descricao": description, "bairro": "Centro"})
            response.raise_for_status()
            actual = response.json()
            if actual.get("fonte_analise") != "llm":
                raise SystemExit("Uma resposta não veio do LLM; evidência não foi registrada como real.")
            results.append({"entrada": description, "categoria_esperada": expected,
                            "obtida": actual, "aprovado": actual.get("categoria_sugerida") == expected})

    assert len(results) == 3 and all(row["obtida"]["fonte_analise"] == "llm" for row in results)
    directory = root / "docs" / "evidencias"
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / f"ia-{now.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    output.write_text(json.dumps({"executado_em_utc": now.isoformat(), "modelo": health["modelo"],
                                  "tipo": "LLM real via API", "casos": results},
                                 ensure_ascii=False, indent=2), encoding="utf-8")

    table = [f"Execução real em {now.isoformat()}, modelo `{health['modelo']}`.",
             "", "| Entrada | Esperado antes do teste | Saída obtida | Ajuste realizado |",
             "|---|---|---|---|"]
    for row in results:
        actual = row["obtida"]
        obtained = f"{actual['categoria_sugerida']}; prioridade {actual['prioridade_sugerida']}"
        adjustment = "Nenhum ajuste após este caso: categoria correspondeu ao esperado." if row["aprovado"] else "Divergência: revisar o prompt e executar novamente; manter este registro."
        table.append(f"| {row['entrada']} | Categoria {row['categoria_esperada']} | {obtained} | {adjustment} |")
    table.extend(["", f"[Respostas completas desta execução]({output.relative_to(root).as_posix()}).",
                  "", "Estes casos sintéticos não estimam acurácia geral nem substituem validação com pessoas."])
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    begin, end = "<!-- IA:INICIO -->", "<!-- IA:FIM -->"
    assert text.count(begin) == text.count(end) == 1
    before, remainder = text.split(begin)
    _, after = remainder.split(end)
    readme.write_text(before + begin + "\n" + "\n".join(table) + "\n" + end + after, encoding="utf-8")
    print(f"Evidência salva: {output.relative_to(root)}")
    for row in results:
        print(f"{'PASS' if row['aprovado'] else 'FAIL'}: {row['categoria_esperada']} -> {row['obtida']['categoria_sugerida']}")
    if not all(row["aprovado"] for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
