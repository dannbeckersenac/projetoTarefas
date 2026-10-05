# Decisões

- Sem Git neste momento: confirmado pelo usuário; não criar branch nem orientar commit.
- O usuário criou o schema MySQL `tarefa_certa` e os arquivos locais de conexão. O código existente escolhe `mysql+mysqlconnector`; preservar essa escolha.
- O contexto anterior previa listas em memória; o usuário agora pediu explicitamente SQLAlchemy e classes ORM, substituindo esse desenho para persistência.
- O venv atual não contém SQLAlchemy nem `mysql-connector-python`, e `requirements.txt` ainda não declara essas dependências. A inclusão depende de aprovação do plano 002.
- Não incluir linter externo sem aprovação; `python -m compileall -q .` verifica sintaxe, não estilo.
- CORS lê a origem de `backend/.env` e permanece sem origens liberadas até o endereço exato do frontend ser definido.
