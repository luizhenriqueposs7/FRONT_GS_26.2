# Vídeo ZelaBairro — fala por fala

Versão técnica montada em 13/11/2026: **5min00s**, com a voz original e complementos enviados pelo grupo, em velocidade natural. [Assistir no YouTube — não listado](https://youtu.be/17K65Aqt3Qs). Os tempos e falas abaixo registram o planejamento de referência; a montagem acompanha os tempos medidos na voz. O MP4 está no ZIP local em `docs/video/ZelaBairro_Final_5min.mp4`, com medições em [video/VERIFICACAO.md](video/VERIFICACAO.md).

## 0:00–0:35 — Problema e público

**Tela:** nome do projeto, integrantes e fonte do IBGE; depois interface inicial.

**Fala 01:** “Uma calçada danificada pode dificultar um trajeto cotidiano. O ZelaBairro organiza relatos de problemas de calçada, iluminação e pavimentação.”

**Fala 02:** “No Censo de 2022, 68,8% dos moradores das áreas com características urbanas pesquisadas viviam em vias sem rampa para cadeirantes. Esse dado do IBGE contextualiza a relevância da acessibilidade urbana.”

**Fala 03:** “Nosso público são moradores e gestores. A proposta se relaciona ao ODS 11, ao apoiar a participação dos cidadãos e o registro de barreiras nos espaços públicos.”

## 0:35–0:55 — Execução

**Tela:** execução real de `docker compose up --build`, serviços saudáveis e diagrama do README. Não mostrar `.env` ou chaves. Este trecho só deve afirmar sucesso depois de verificar Docker em uma máquina disponível.

**Fala 04:** “O projeto separa interface Streamlit e API FastAPI. O SQLite guarda os registros e o provedor de IA fica apenas no back-end.”

**Fala 05:** “O Docker Compose reúne os dois serviços, com rede interna e volume para os dados. Esta execução mostra a aplicação disponível fora do ambiente de desenvolvimento.”

Se Docker ainda não foi executado, substituir a segunda fala por: “A configuração Docker está preparada, mas sua execução ainda precisa ser verificada.” Essa alternativa não comprova o requisito completo.

## 0:55–1:55 — Entrada, IA e revisão humana

**Tela:** bairro Centro; relato “Poste apagado e fio exposto na calçada.”; analisar; spinner; resposta real; alterar e revisar prioridade; confirmar; enviar; protocolo. Não usar modo demonstrativo neste trecho.

**Fala 06:** “Vou registrar um relato fictício de iluminação, usando uma referência pública e sem informar endereço residencial.”

**Fala 07:** “O formulário valida os campos e indica a espera. A API envia o relato para um LLM real na Groq.”

**Fala 08:** “O modelo devolve categoria, prioridade, resumo e justificativa em JSON. O Pydantic valida essa estrutura antes de apresentar a sugestão.”

**Fala 09:** “O cidadão pode corrigir a categoria, a prioridade e o resumo. A confirmação pertence a esta análise: uma nova sugestão exige uma nova revisão.”

**Fala 10:** “Após confirmar, o sistema registra o relato e gera um protocolo. Isso representa um registro nesta prova de conceito, sem abertura automática de atendimento municipal.”

## 1:55–2:30 — Histórico, gestão e gráfico

**Tela:** Minhas solicitações; painel da gestão com chave oculta; hover e zoom; filtros de categoria e status com dados sintéticos variados; atualização do andamento e atualização do histórico.

**Fala 11:** “O botão Acompanhar meu relato abre o histórico da sessão, em Minhas solicitações. Cada status tem uma explicação. O botão Atualizar busca mudanças feitas pela gestão.”

**Fala 12:** “Na gestão, o gráfico Plotly apresenta os registros. Estes dois filtros alteram a visualização por categoria e por status.”

**Fala 13:** “A gestão atualiza o andamento e pode deixar uma observação. O cidadão acompanha essa informação pelo protocolo.”

## 2:30–2:50 — Falha tratada

**Tela:** interromper somente a API em ambiente de demonstração; solicitar atualização; mostrar mensagem compreensível; reiniciar o serviço. Não desligar serviços usados por outras pessoas.

**Fala 14:** “Com a API temporariamente indisponível, a interface informa o problema sem mostrar detalhes internos. Timeouts e respostas inválidas da IA também recebem tratamento.”

## 2:50–3:40 — Código e autoria

**Tela:** árvore do projeto, provedor LLM, schemas, state/session.py, cliente HTTP, `.env.example` e `.gitignore`. Mostrar código legível, sem abrir o `.env` real.

**Fala 15:** “As telas estão em features, os componentes em ui, o estado em state e o cliente HTTP em providers. O back-end separa rotas, schemas, pipeline e provedores.”

**Fala 16:** “Escolhemos Streamlit para construir formulários e gráficos em Python. O prompt limita as respostas ao domínio e o Pydantic restringe os valores aceitos.”

**Fala 17:** “O session_state mantém o identificador, a análise pendente e o histórico. O cache reutiliza a conexão e as consultas, separadas por cidadão e autorização.”

**Fala 18:** “Ao criar ou atualizar um relato, o cache correspondente é invalidado. Alterar filtros não chama o LLM novamente.”

**Fala 19:** “A chave da Groq é lida do ambiente no back-end. O arquivo de segredos fica fora do Git e do pacote de entrega.”

## 3:40–4:30 — Evidências e aprendizado

**Tela:** tabela real de IA do README e JSON completo; depois tabela de usabilidade e antes/depois de um ajuste efetivamente decorrente do feedback.

**Fala 20:** “Executamos três casos reais com o modelo GPT OSS de vinte bilhões de parâmetros na Groq. Os relatos de buraco, iluminação e calçada retornaram as categorias esperadas. As respostas completas estão preservadas nesta evidência.”

**Fala 21:** “Os testes automatizados verificam validação, API, erros de comunicação, cache e revisão humana. São verificações técnicas, não substitutos para os testes com pessoas.”

**Fala 22:** “Os três participantes relataram dúvidas sobre edição, acompanhamento e status. Com esse feedback, destacamos o protocolo, criamos um acesso direto ao histórico e adicionamos resumo editável e explicações. Os ajustes foram verificados tecnicamente; um reteste com os participantes ainda não foi registrado.”

As observações de P1/P2/P3 estão em `docs/evidencias/usabilidade-20261113.md`, com a comparação visual da base entregue. Se mencionar a edição do resumo por P3, explicar que, segundo o grupo, ela utilizou outra versão, não fornecida para análise. A gravação de 13/11 incorpora os registros e ajustes com narração complementar; a origem de 12/11 permanece preservada no projeto local de montagem.

## 4:30–4:50 — Limites e encerramento

**Tela:** limitações e links reais do repositório/vídeo, quando disponíveis.

**Fala 23:** “A IA pode errar ou reproduzir vieses. A revisão humana reduz esse risco, mas não comprova a verdade de um relato nem substitui a avaliação do órgão responsável.”

**Fala 24:** “O ZelaBairro torna o registro e o acompanhamento mais compreensíveis. Esta prova de conceito não atende emergências nem promete prazo de reparo.”

## Fontes

- Problema: [IBGE](https://educa.ibge.gov.br/jovens/materias-especiais/22746-censo-2022-revela-que-88-5-dos-moradores-moravam-em-vias-pavimentadas.html).
- Relação proposta com sustentabilidade: [ONU Brasil — ODS 11](https://brasil.un.org/pt-br/sdgs/11).
- Resultados da IA: tabela e arquivo JSON da execução real vinculados no README.

Antes da submissão: conferir os dados de coleta sinalizados no relatório, ouvir as junções da narração e enviar no Portal o repositório e o link do vídeo já hospedado. As credenciais e os áudios originais permanecem fora do pacote.
