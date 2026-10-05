# Tarefa Certa

Projeto local de API e interface para acompanhar pedidos internos por checklist.

## Backend

No PowerShell:

```powershell
Set-Location backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\fastapi.exe dev main.py
```

Documentação da API: `http://127.0.0.1:8000/docs`.

## Frontend

A pasta `frontend/` ainda não tem aplicação executável. A configuração React e seus comandos serão adicionados após aprovar as dependências específicas do frontend.

## Documentação

- `REGRAS.md`: regras de desenvolvimento.
- `.docs/`: arquitetura, roadmap, decisões, próximos passos e deploy local.
- `docs/CONTEXTO.md`: contexto recebido para o projeto.
- `docs/CARTILHA.md`: cartilha original, ainda pendente de confirmação/entrega.
