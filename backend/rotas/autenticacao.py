# Rota de login. Recebe e-mail e senha em JSON e devolve o token JWT.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from banco import obter_sessao
from esquemas.usuario import LoginEntrada, Token
from seguranca import criar_token
from servicos import usuario as servico_usuario

router = APIRouter(tags=["autenticacao"])
# No Swagger, o Authorize pede só o token: cole o access_token devolvido pelo /login.
esquema_bearer = HTTPBearer(auto_error=False)


@router.post("/login", response_model=Token)
def login(dados: LoginEntrada, sessao=Depends(obter_sessao)):
    usuario = servico_usuario.autenticar(sessao, dados.email, dados.senha)
    if usuario is None:                             # e-mail ou senha: a mesma resposta
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    return {"access_token": criar_token(usuario.id), "token_type": "bearer"}


# Dependência das rotas protegidas: lê o token do Authorization e devolve o usuário.
# Sem token, devolve 401.
def obter_usuario_atual(
        credenciais: HTTPAuthorizationCredentials | None = Depends(esquema_bearer),
        sessao=Depends(obter_sessao)):
    if credenciais is None:
        raise HTTPException(status_code=401, detail="Token não enviado",
                            headers={"WWW-Authenticate": "Bearer"})
    usuario = servico_usuario.usuario_do_token(sessao, credenciais.credentials)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Token inválido ou vencido")
    return usuario


# Aula 10 · grupos: a dependência que protege a rota por permissão.
# Ela é uma "fábrica de dependências": exigir_permissao("tarefas:criar") não confere
# nada ainda, só DEVOLVE uma função (verificar) que já sabe qual permissão pedir.
# Quem chama o verificar é o FastAPI, a cada requisição. Na rota fica assim:
#     usuario=Depends(exigir_permissao("tarefas:criar"))
# A ordem das respostas:
#   - sem token ou token ruim       → 401 (vem do obter_usuario_atual)
#   - com login, sem a permissão    → 403 (o servidor sabe quem é, mas o grupo não pode)
#   - com a permissão               → devolve o usuário para a rota, como o obter_usuario_atual
def exigir_permissao(permissao: str):
    def verificar(usuario=Depends(obter_usuario_atual)):
        if not servico_usuario.tem_permissao(usuario, permissao):
            raise HTTPException(status_code=403,
                                detail="Seu grupo não tem permissão para esta ação")
        return usuario
    return verificar
