from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone   # data com hora, e uma duração
from configuracao import obter_configuracao

hasher = PasswordHash.recommended()

def gerar_hash(senha: str):                    # no cadastro
    return hasher.hash(senha)
def verificar_senha(senha: str, senha_hash: str):  # no login: True ou False
    return hasher.verify(senha, senha_hash)

configuracao = obter_configuracao()

def criar_token(usuario_id: int):
    validade = datetime.now(timezone.utc) + timedelta(minutes=60)  # agora mais uma hora
    dados = {"sub": str(usuario_id), "exp": validade}         # quem é, e quando vence
    return jwt.encode(dados, configuracao["chave_do_token"], algorithm="HS256")     

def ler_token(token: str):
    try:
        dados = jwt.decode(token, configuracao["chave_do_token"], algorithms=["HS256"])
    except jwt.InvalidTokenError:          # lacre falso, ou pulseira vencida
        return None
    return int(dados["sub"])                # o id de quem fez a requisição