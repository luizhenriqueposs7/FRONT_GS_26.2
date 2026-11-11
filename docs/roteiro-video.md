# Vídeo ZelaBairro — fala por fala

Planejamento de até 4min50s, com dez segundos de margem. Os tempos precisam ser confirmados com o áudio real. Gravar cada fala numerada separadamente, na ordem, sem ler as instruções de tela. A montagem deve acompanhar a voz na velocidade natural.

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

**Fala 09:** “O cidadão pode corrigir a categoria e a prioridade. A confirmação pertence a esta análise: uma nova sugestão exige uma nova revisão.”

**Fala 10:** “Após confirmar, o sistema registra o relato e gera um protocolo. Isso representa um registro nesta prova de conceito, sem abertura automática de atendimento municipal.”

## 1:55–2:30 — Histórico, gestão e gráfico

**Tela:** Minhas solicitações; painel da gestão com chave oculta; hover e zoom; filtros de categoria e status com dados sintéticos variados; atualização do andamento e atualização do histórico.

**Fala 11:** “O histórico fica no estado da sessão e é apresentado em Minhas solicitações. O botão Atualizar busca mudanças feitas pela gestão.”

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

**Fala 22 — somente após validar com pessoas:** “Testamos com três participantes próximos do público-alvo. A principal dificuldade observada foi [observação real]. A partir desse feedback, alteramos [ajuste real] e verificamos [resultado real].”

Enquanto os testes estiverem pendentes, usar: “A validação com três participantes ainda está pendente; o roteiro e a ficha estão preparados. Não apresentamos esse item como concluído.” Essa fala é transparente, mas o requisito continuará pendente.

## 4:30–4:50 — Limites e encerramento

**Tela:** limitações e links reais do repositório/vídeo, quando disponíveis.

**Fala 23:** “A IA pode errar ou reproduzir vieses. A revisão humana reduz esse risco, mas não comprova a verdade de um relato nem substitui a avaliação do órgão responsável.”

**Fala 24:** “O ZelaBairro torna o registro e o acompanhamento mais compreensíveis. Esta prova de conceito não atende emergências nem promete prazo de reparo.”

## Fontes

- Problema: [IBGE](https://educa.ibge.gov.br/jovens/materias-especiais/22746-censo-2022-revela-que-88-5-dos-moradores-moravam-em-vias-pavimentadas.html).
- Relação proposta com sustentabilidade: [ONU Brasil — ODS 11](https://brasil.un.org/pt-br/sdgs/11).
- Resultados da IA: tabela e arquivo JSON da execução real vinculados no README.

Pendências antes da versão final: vídeo com execução Docker comprovada; resultados reais de três participantes; links de entrega; áudio e sincronização final. Não gravar credenciais ou informações pessoais.
