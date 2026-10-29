# Rotas de usuários. Aqui só entra HTTP: status, HTTPException e esquemas.
# Toda rota pede a sessão com sessao=Depends(obter_sessao) e passa adiante:
# rota, serviço, repositório.
from fastapi import APIRouter, Depends, HTTPException

from banco import obter_sessao
from esquemas.usuario import UsuarioCriar, UsuarioSaida
from rotas.autenticacao import exigir_permissao, obter_usuario_atual   # Aula 10 · grupos: + exigir_permissao
from servicos import usuario as servico

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


# Cadastra um usuário. Fica aberta, sem token: é por aqui que a conta nasce.
# 201 com o usuário criado, sem a senha (o UsuarioSaida não tem esse campo).
# Aula 10 · grupos: o corpo traz "grupo" no lugar de "tipo". Atenção: a rota é aberta,
# então qualquer pessoa ainda pode se cadastrar como executor (risco anotado no plano 004).
@router.post("", response_model=UsuarioSaida, status_code=201)
def criar_usuario(dados: UsuarioCriar, sessao=Depends(obter_sessao)):
    resultado = servico.criar(sessao, dados)
    # O serviço devolve texto quando recusa: e-mail repetido vira 409 (conflito).
    # Aula 10 · grupos: "Grupo não cadastrado" (migration não aplicada) também cai aqui.
    if isinstance(resultado, str):
        raise HTTPException(status_code=409, detail=resultado)
    return resultado


# Lista os usuários. Só para quem fez login.
# Aula 10 · grupos: e só para o grupo com "usuarios:listar" (executor). Solicitante: 403.
@router.get("", response_model=list[UsuarioSaida])
def listar_usuarios(usuario=Depends(exigir_permissao("usuarios:listar")), sessao=Depends(obter_sessao)):
    return servico.listar(sessao)


# Mostra quem está logado. Fica antes do /{usuario_id}: senão o "eu" seria lido como id.
# Aula 10 · grupos: continua pedindo só o login. Todo grupo pode ver os próprios dados,
# e a resposta mostra o grupo: {"grupo": {"id": 1, "nome": "solicitante"}}.
@router.get("/eu", response_model=UsuarioSaida)
def ver_usuario_atual(usuario=Depends(obter_usuario_atual)):
    return usuario


# Mostra um usuário. Só para quem fez login; 404 quando o id não existe.
# Aula 10 · grupos: e só para o grupo com "usuarios:ver" (executor). Solicitante: 403.
@router.get("/{usuario_id}", response_model=UsuarioSaida)
def ver_usuario(usuario_id: int, usuario=Depends(exigir_permissao("usuarios:ver")),
                sessao=Depends(obter_sessao)):
    encontrado = servico.buscar_por_id(sessao, usuario_id)   # usuario é quem fez login
    if encontrado is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return encontrado
