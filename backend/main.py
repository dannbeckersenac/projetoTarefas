# O ponto de entrada cria a aplicação e reúne as rotas dos recursos. Nenhuma rota aqui.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configuracao import obter_configuracao
from rotas import autenticacao, itens, tarefas, usuarios

configuracao = obter_configuracao()

# Cria o app para que o FastAPI publique a API e a documentação em /docs.
app = FastAPI(title="Tarefa Certa")

# Limita chamadas do navegador à origem exata do front, lida do .env (nunca "*").
app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracao["origem_frontend"]] if configuracao["origem_frontend"] else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include_router liga as rotas que moram em rotas/tarefas.py, rotas/itens.py e rotas/usuarios.py.
app.include_router(tarefas.router)
app.include_router(itens.router)
app.include_router(usuarios.router)
app.include_router(autenticacao.router)
