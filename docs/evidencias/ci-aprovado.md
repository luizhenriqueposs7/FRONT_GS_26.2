# Execução externa aprovada

- Repositório: https://github.com/luizhenriqueposs7/FRONT_GS_26.2
- Código verificado: `4764f740cfe491e930143a87f8ce35f49796524f`.
- Resultado público: https://github.com/luizhenriqueposs7/FRONT_GS_26.2/actions/runs/43371755289
- `testes`: sucesso; 42 testes passaram no ambiente Linux/Python 3.12 com as dependências instaladas pelo workflow.
- `docker`: sucesso; as imagens foram construídas, os serviços iniciaram e a API e a interface responderam às verificações.

O smoke test Docker usa `DEMO_MODE=true` e credencial sintética de gestão; não contém a chave Groq. A integração real com o LLM foi verificada separadamente e consta nos JSONs de IA desta pasta. Nenhuma dessas execuções foi apresentada como teste de usabilidade com pessoas.

Atualizações posteriores restritas a documentação não alteram o código que este resultado verificou.
