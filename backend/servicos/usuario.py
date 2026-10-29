# Serviço de usuários: as decisões do cadastro. Nada de HTTPException nem status code aqui.
# Quando recusa, devolve um texto com o motivo, e a rota escolhe o status.
from esquemas.usuario import UsuarioCriar
from repositorios import grupo as repositorio_grupo   # Aula 10 · grupos: para achar o grupo pelo nome
from repositorios import usuario as repositorio
from seguranca import gerar_hash, ler_token, verificar_senha


# Cadastra um usuário: confere se o e-mail está livre e troca a senha pelo hash.
def criar(sessao, dados: UsuarioCriar):
    if repositorio.buscar_por_email(sessao, dados.email) is not None:
        return "E-mail já cadastrado"
    # Aula 10 · grupos: o pattern do esquema já garante o nome. Se mesmo assim o grupo
    # não estiver no banco, a migration de grupos não foi aplicada.
    grupo = repositorio_grupo.buscar_por_nome(sessao, dados.grupo)
    if grupo is None:
        return "Grupo não cadastrado"
    usuario = dados.model_dump()                     # o esquema vira dicionário
    usuario["senha"] = gerar_hash(usuario["senha"])  # a senha em texto puro nunca vai para o banco
    # Aula 10 · grupos: a tabela não tem coluna "grupo", tem grupo_id. Troca o nome pelo id.
    del usuario["grupo"]
    usuario["grupo_id"] = grupo.id
    return repositorio.salvar(sessao, usuario)


# Lista os usuários. O serviço só repassa.
def listar(sessao):
    return repositorio.listar(sessao)


# Busca um usuário. Devolve None quando não existe; a rota transforma isso em 404.
def buscar_por_id(sessao, usuario_id: int):
    return repositorio.buscar_por_id(sessao, usuario_id)


# Confere e-mail e senha. Devolve o usuário, ou None se o e-mail não existir
# ou a senha não conferir. O token quem cria é a rota.
def autenticar(sessao, email: str, senha: str):
    usuario = repositorio.buscar_por_email(sessao, email)
    if usuario is None or not verificar_senha(senha, usuario.senha):
        return None
    return usuario


# Descobre quem fez a requisição. Devolve None se o token for inválido, estiver vencido
# ou apontar para um usuário que não existe mais.
def usuario_do_token(sessao, token: str):
    usuario_id = ler_token(token)
    if usuario_id is None:
        return None
    return repositorio.buscar_por_id(sessao, usuario_id)


# Aula 10 · grupos: a pergunta central do controle de acesso: "o grupo desta pessoa
# tem esta permissão?". Lê as permissões pelos dois relationships:
#   usuario.grupo             → o Grupo dele (pelo grupo_id)
#   usuario.grupo.permissoes  → a lista de Permissao do grupo (pela tabela do meio)
# Devolve True ou False. Quem transforma o False em 403 é a rota.
def tem_permissao(usuario, permissao: str):
    return any(p.nome == permissao for p in usuario.grupo.permissoes)
