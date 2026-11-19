# Requisitos e evidências da entrega

| Requisito | Implementação ou evidência |
|---|---|
| Fluxo CitizenTech com IA | Streamlit → FastAPI → Groq; saída estruturada e protocolo após revisão humana. |
| Arquitetura | Front-end e back-end em camadas, com comunicação HTTP e diagrama no README. |
| Estado e cache | Histórico na sessão, consultas por identidade/autorização e invalidação após alterações. |
| Validação e falhas | Pydantic, campos obrigatórios, limites de tamanho e mensagens para falhas de rede, timeout e resposta inválida. |
| Segredos e CORS | Configuração por ambiente, .env.example e origens restritas; a chave do LLM permanece no back-end. |
| Revisão humana | Categoria, prioridade e resumo editáveis; confirmação específica para cada análise. |
| Visualização | Plotly com hover e zoom, filtros por categoria e status e componentes reutilizados. |
| Acessibilidade | Rótulos, texto e ícones, indicação de espera e explicações dos status. Cuidados descritos no README. |
| Testes automatizados | 42 testes; relatório em [docs/evidencias/testes.xml](docs/evidencias/testes.xml). |
| Validação da IA | Três casos reais, ajuste do prompt e reteste em [docs/evidencias/ajuste-prompt.md](docs/evidencias/ajuste-prompt.md). |
| Validação com pessoas | Roteiro em [docs/validacao.md](docs/validacao.md); observações, limites e ajustes em [docs/evidencias/usabilidade-20261113.md](docs/evidencias/usabilidade-20261113.md). |
| Execução externa | Docker Compose com instruções no README e [verificação aprovada no GitHub Actions](https://github.com/luizhenriqueposs7/FRONT_GS_26.2/actions/runs/43636895337). |
| Código-fonte | [Repositório público](https://github.com/luizhenriqueposs7/FRONT_GS_26.2). |
| Vídeo | [Demonstração de 5min00s no YouTube, não listada](https://youtu.be/17K65Aqt3Qs). |

Para a submissão, usar o link do repositório e o link do vídeo.
