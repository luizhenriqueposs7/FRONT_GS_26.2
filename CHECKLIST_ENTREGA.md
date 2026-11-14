# Conferência da entrega

| Item do enunciado | Situação verificável |
|---|---|
| Streamlit → FastAPI → LLM real → resposta estruturada | Executado com Groq; respostas reais em docs/evidencias/ia-*.json. |
| Arquitetura em camadas | Preservada e documentada no README, com diagrama. |
| Estado, histórico e cache | Histórico na sessão; cache de consultas por identidade/autorização; invalidação após alterações. |
| Robustez e validação | Espaços normalizados, campos vazios rejeitados e falhas tratadas. Listas com formato, campos, tipos ou status inválidos são rejeitadas no cliente HTTP, antes de chegar às telas. |
| Revisão humana | Nova confirmação a cada análise; falha descarta a sugestão antiga. O callback de uma nova análise limpa a mensagem de sucesso e o protocolo anteriores antes do rerun. Regressões verificadas com AppTest. |
| Plotly e dois filtros | Implementados; categorias/status alteram o gráfico. |
| Testes automatizados | 42 testes passaram em 13/11/2026; relatório em docs/evidencias/testes.xml. |
| Justificativa, fonte, ODS e ética | README completo para o escopo da POC; sem alegações de impacto medido. |
| Três casos reais da IA | Executados; primeiro resultado, ajuste do prompt e reteste preservados. |
| Três pessoas e ajuste decorrente de feedback | Registros de P1/P2/P3 fornecidos pelo grupo, referentes à versão anterior às correções. Ajustes implementados e verificados; observações, comentários e comparação visual em docs/evidencias/usabilidade-20261113.md. |
| Contexto da coleta | Data e identificadores das versões não informados. O grupo confirmou que P3 editou o resumo em outra versão, não fornecida nem identificada por commit. Na base entregue, o recurso foi implementado nesta revisão. Reteste com participantes após os ajustes não informado. |
| Docker funcionando | Construção, inicialização e endpoints aprovados fora da máquina local no GitHub Actions: https://github.com/luizhenriqueposs7/FRONT_GS_26.2/actions/runs/43373610251. O vídeo apresenta os logs reais dessa execução. |
| GitHub público | Código e evidências publicados em https://github.com/luizhenriqueposs7/FRONT_GS_26.2. A chave privada não foi publicada. |
| Vídeo até cinco minutos | Nova versão técnica de 13/11/2026: 300 segundos, 1600 × 900, 25 fps, H.264/AAC, voz natural. Mostra as correções e as evidências de usabilidade; fala antiga sobre testes humanos pendentes removida. Incluído no ZIP local em docs/video/ZelaBairro_Final_5min.mp4, com medições em docs/video/VERIFICACAO.md. |
| Publicação e acesso ao vídeo | [Vídeo publicado no YouTube](https://youtu.be/17K65Aqt3Qs) como não listado, com duração exibida de 5min00s. Página e início da reprodução conferidos em 14/11/2026; link incluído no README. |
| Comentários de preparação no código | Removidas as quatro marcações de roteiro; documentação das funções preservada. |

O código, o vídeo atualizado e o pacote local estão preparados para revisão, com o vídeo hospedado e vinculado no README. Antes da submissão, conferir os dados de coleta sinalizados no relatório e ouvir as junções da narração. O envio no Portal não foi realizado por esta conferência, que não representa nota oficial.
