# A porta de entrada da API na Vercel. A Vercel roda como Function o que estiver em api/,
# e o vercel.json manda para cá tudo que chega em /api/...
# Faz o papel do handle_path do Caddyfile: o app de backend/main.py é montado em /api,
# então /api/tarefas chega nas rotas como /tarefas.
import sys
from pathlib import Path

from fastapi import FastAPI

# O backend importa os módulos pelo nome curto (from configuracao import ...),
# então a pasta backend/ entra no caminho de busca do Python.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from main import app as api_tarefa_certa  # noqa: E402

app = FastAPI()
app.mount("/api", api_tarefa_certa)
