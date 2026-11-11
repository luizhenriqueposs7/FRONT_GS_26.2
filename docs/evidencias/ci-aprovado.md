# Execução externa aprovada

- Repositório: https://github.com/luizhenriqueposs7/FRONT_GS_26.2
- Código verificado: `2eab16a89903e347ea3b9ccb3855bb8fc9ab2512`.
- Resultado público: https://github.com/luizhenriqueposs7/FRONT_GS_26.2/actions/runs/42948346515
- `testes`: sucesso; 28 testes passaram no ambiente Linux/Python 3.12 com as dependências instaladas pelo workflow.
- `docker`: sucesso; as imagens foram construídas, os serviços iniciaram e a API e a interface responderam às verificações.

O smoke test Docker usa `DEMO_MODE=true` e credencial sintética de gestão; não contém a chave Groq. A integração real com o LLM foi verificada separadamente e consta nos JSONs de IA desta pasta. Nenhuma dessas execuções foi apresentada como teste de usabilidade com pessoas.

Uma falha anterior revelou um acesso interno de AppTest alterado em versão nova e uma corrida entre inicialização e consulta da interface. O teste passou a usar o acesso público ao estado e o Compose passou a aguardar o healthcheck da interface. O link acima registra o reteste bem-sucedido.

Atualizações posteriores restritas a documentação não alteram o código que este resultado verificou.
