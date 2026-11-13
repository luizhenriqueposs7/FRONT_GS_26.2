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
| Contexto da coleta | Data e identificador da versão não informados. Edição do resumo citada por P3 aguarda confirmação; o recurso foi implementado nesta revisão. Reteste com participantes após os ajustes não informado. |
| Docker funcionando | Construção, inicialização e endpoints aprovados fora da máquina local no GitHub Actions: https://github.com/luizhenriqueposs7/FRONT_GS_26.2/actions/runs/43368906764. O vídeo apresenta a evidência dessa execução. |
| GitHub público | Código e evidências publicados em https://github.com/luizhenriqueposs7/FRONT_GS_26.2. A chave privada não foi publicada. |
| Vídeo até cinco minutos | Arquivo existente verificado: 300 segundos, 1600 × 900, H.264/AAC. Incluído no ZIP local em docs/video/ZelaBairro_Final_5min.mp4. A gravação antecede os ajustes de usabilidade e deve ser atualizada para mostrar as novas evidências. |
| Publicação e acesso ao vídeo | Pendente: manter o arquivo local até definir a hospedagem, publicar no YouTube como não listado ou no repositório e inserir o link no README. |
| Comentários de preparação no código | Removidas as quatro marcações de roteiro; documentação das funções preservada. |

O código e o pacote local estão preparados para revisão. Antes da submissão, conferir os dados de coleta sinalizados no relatório e atualizar/publicar o vídeo com os registros de usabilidade e os ajustes. Esta conferência não representa nota oficial.
