# Aula 6 · Um arquivo só para o banco (slide 21).
# As peças do SQLAlchemy: Engine, Sessão e Base. O Modelo fica em modelos/.
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from configuracao import obter_configuracao

configuracao = obter_configuracao()

# Engine: sabe onde o banco está e abre as conexões. Um só no projeto inteiro.
engine = create_engine(configuracao["url_do_banco"])  # o motor

# Sessao: a fábrica de conversas. Cada Sessao() abre uma conversa com o banco:
# abre, pede, grava e fecha. Faz o papel do abrir_conexao() do mysql.connector.
Sessao = sessionmaker(bind=engine)


# Base: a classe mãe dos modelos. Todo modelo herda dela,
# como o esquema Pydantic herda de BaseModel.
class Base(DeclarativeBase):
    pass  # o corpo fica vazio de propósito
