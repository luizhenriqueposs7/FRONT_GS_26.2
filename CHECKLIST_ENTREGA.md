# Conferência da entrega

| Item do enunciado | Situação verificável |
|---|---|
| Streamlit → FastAPI → LLM real → resposta estruturada | Executado com Groq; respostas reais em docs/evidencias/ia-*.json. |
| Arquitetura em camadas | Preservada e documentada no README, com diagrama. |
| Estado, histórico e cache | Histórico na sessão; cache de consultas por identidade/autorização; invalidação após alterações. |
| Robustez e validação | Espaços normalizados, campos vazios rejeitados, falhas tratadas; regressões automatizadas. |
| Revisão humana | Nova confirmação a cada análise; falha descarta resultado anterior. Verificado com AppTest e no navegador. |
| Plotly e dois filtros | Implementados; categorias/status alteram o gráfico. |
| Testes automatizados | 28 testes passaram; relatório em docs/evidencias/testes.xml. |
| Justificativa, fonte, ODS e ética | README completo para o escopo da POC; sem alegações de impacto medido. |
| Três casos reais da IA | Executados; primeiro resultado, ajuste do prompt e reteste preservados. |
| Três pessoas e ajuste decorrente de feedback | Pendente de observações reais. Preencher README e docs/validacao.md após a aplicação. |
| Docker funcionando | Construção, inicialização e endpoints aprovados fora da máquina local no GitHub Actions: https://github.com/luizhenriqueposs7/FRONT_GS_26.2/actions/runs/42948346515. Incluir essa demonstração no vídeo. |
| GitHub público | Código e evidências publicados em https://github.com/luizhenriqueposs7/FRONT_GS_26.2. A chave privada não foi publicada. |
| Vídeo até cinco minutos | Roteiro fala por fala em docs/roteiro-video.md; gravação/montagem final e áudio ainda pendentes. |

O código corrigido e a documentação não asseguram nota oficial. Para pleitear os 10 pontos, concluir também as evidências humanas, execução Docker e vídeo solicitados pelo enunciado.
