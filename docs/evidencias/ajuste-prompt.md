# Ajuste baseado em execução real do LLM

Data local: 10/11/2026. Modelo: `openai/gpt-oss-20b`, na Groq. Relatos sintéticos; nenhuma pessoa foi apresentada como participante.

## Evidência anterior

[Primeira execução completa](ia-20261111T023047438259Z.json).

Entrada: “Há um buraco grande no asfalto perto da praça.”

A categoria foi Buraco, mas a justificativa incluiu “especialmente em área de alto tráfego próximo à praça” e recomendou reparo imediato. O volume de tráfego não foi informado. Também houve prioridade Alta em casos sem gravidade explícita suficiente segundo a política escolhida para a POC.

## Ajuste realizado

Em `backend/providers/llm.py`, o prompt passou a:

- proibir inventar trânsito, frequência, acidentes, intensidade de dano ou prazo;
- usar Alta quando houver perigo concreto relatado, como fio exposto, acidente, queda ou passagem bloqueada;
- usar Média quando não houver gravidade explicitamente sustentada;
- limitar a justificativa a duas frases curtas apoiadas no texto, sem anunciar atendimento oficial.

## Reteste observado

[Segunda execução completa](ia-20261111T023643086464Z.json).

| Caso | Categoria | Prioridade após ajuste | Justificativa observada |
|---|---|---|---|
| Buraco no asfalto perto da praça | Buraco | Média | Relato menciona buraco grande no asfalto perto da praça, indicando possível risco de acidentes. |
| Poste apagado e fio exposto | Iluminação | Alta | O relato menciona poste apagado e fio exposto na calçada, indicando risco de choque elétrico e queda. |
| Calçada quebrada, passagem dificultada | Calçada | Média | Relato indica calçada quebrada e que dificulta a passagem. |

A referência a alto tráfego deixou de aparecer no reteste. As categorias permaneceram coerentes com as expectativas anteriores. A menção a riscos ainda é interpretação do modelo; não representa acidente constatado nem garantia de correção em outros relatos. A revisão humana permanece obrigatória. Três casos não estimam acurácia geral nem substituem teste com três pessoas.
