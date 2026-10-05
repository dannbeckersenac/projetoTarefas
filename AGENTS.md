# Tarefa Certa

API e interface para abrir pedidos internos, acompanhar seus checklists e registrar etapas concluídas. O MVP atende solicitantes e executores de um escritório pequeno.

## Stack e comandos
- Stack: Python 3, FastAPI, Pydantic, React e `fetch`.
- Dependências do backend: `fastapi[standard]`, `python-dotenv` e `pytest`.
- Preparar ambiente (PowerShell, na pasta `backend`): `python -m venv venv` e `.\venv\Scripts\python.exe -m pip install -r requirements.txt`
- Rodar API (na pasta `backend`): `.\venv\Scripts\fastapi.exe dev main.py`
- Testar backend (na pasta `backend`): `pytest`
- Verificação sintática (na pasta `backend`): `python -m compileall -q .`
- Frontend: os comandos serão registrados quando a configuração React for aprovada e criada.

## Estrutura
- `docs/`: cartilha, briefing, marca e styleguide.
- `frontend/`: aplicação React e as telas da cartilha.
- `backend/rotas/`: endpoints e tradução de resultados para respostas HTTP.
- `backend/servicos/`: decisões e regras da cartilha.
- `backend/repositorios/`: listas em memória e operações de leitura e gravação.
- `backend/esquemas/`: modelos Pydantic de entrada e saída.
- `backend/testes/`: testes da API via TestClient.
- `.docs/`: arquitetura, planejamento e procedimentos do projeto.

## Regras para agentes executores
- A tarefa está no plano indicado no briefing, em `.docs/planos/`. Leia-o inteiro antes de começar.
- Edite somente os arquivos listados no plano aprovado.
- Nunca altere testes, instale dependências, crie arquivos não pedidos ou renomeie arquivos.
- Use exatamente os nomes e assinaturas do contrato.
- Se algo estiver ambíguo, pare e pergunte.

## Regras para o agente de deploy
- Execute somente o roteiro de `.docs/deploy.md`.
- Nunca apague volumes, bancos ou dados.

## Regras para o agente tester
- Execute os cenários do plano indicado exatamente como escritos.
- Nunca edite código nem testes; só observe e reporte.


