# O único arquivo que lê o .env. O resto do projeto pede os valores por obter_configuracao().
import os

from dotenv import load_dotenv
from sqlalchemy import URL

# Carrega as chaves de backend/.env para dentro do os.getenv.
load_dotenv()


def obter_configuracao():
    # Aula 6 · "a outra forma" (slide 19): as peças do banco ficam separadas no .env
    # e o URL.create monta o endereço. Equivale a escrever a linha inteira:
    # postgresql+psycopg2://usuario:senha@localhost:5432/tarefa_certa
    # Vantagem: senha com @ não quebra o endereço, o URL.create resolve.
    url_do_banco = URL.create(
        "postgresql+psycopg2",                        # tipo do banco + driver (o psycopg2, pacote psycopg2-binary)
        username=os.getenv("BANCO_USUARIO"),
        password=os.getenv("BANCO_SENHA"),            # a senha mora no .env, nunca no código
        host=os.getenv("BANCO_HOST"),
        port=int(os.getenv("BANCO_PORTA", "5432")),   # o .env só guarda texto; a porta precisa ser número
        database=os.getenv("BANCO_NOME"),
    )
    # Um dicionário com tudo que muda de máquina para máquina.
    return {
        # CORS liberado só para o endereço exato do front (aula 5).
        "origem_frontend": os.getenv("ORIGEM_FRONTEND", ""),
        # Aula 6: o endereço do banco, que o banco.py usa para criar o engine.
        "url_do_banco": url_do_banco,
        "chave_do_token": os.getenv("CHAVE_DO_TOKEN"),
        # A Vercel define VERCEL=1 nas Functions. Lá não se guarda conexão aberta entre
        # requisições: quem mantém o pool é o pooler do Supabase (porta 6543).
        "sem_pool_de_conexoes": os.getenv("VERCEL") == "1",
    }
