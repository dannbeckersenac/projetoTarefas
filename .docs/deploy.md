# Deploy local

## Subir
1. No PowerShell, acesse a pasta do backend: `Set-Location backend`.
2. Crie o ambiente virtual: `python -m venv venv`.
3. Instale as dependências usando diretamente o Python do ambiente: `.\venv\Scripts\python.exe -m pip install -r requirements.txt`.
4. Suba a API usando o executável do FastAPI no ambiente: `.\venv\Scripts\fastapi.exe dev main.py`.

## Verificar
- Healthcheck: `Invoke-WebRequest -Uri http://127.0.0.1:8000/docs -UseBasicParsing` → esperado: status HTTP 200 e documentação interativa do FastAPI.
- Logs: observar o terminal do servidor → não deve conter traceback ou falha de inicialização.

## Derrubar
- No terminal do servidor, pressione `Ctrl+C`.

## Voltar à versão anterior
- Git ainda não está configurado. Depois da inicialização do repositório, usar `git switch <branch ou commit anterior>` e repetir “Subir”.

## Proibido
- Apagar dados ou arquivos do projeto.
- Editar código ou configuração durante o roteiro.
- Acessar qualquer servidor remoto.
