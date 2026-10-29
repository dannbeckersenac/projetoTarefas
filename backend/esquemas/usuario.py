# Esquemas Pydantic do usuário: conferem o que entra e moldam o que sai da API.
from pydantic import BaseModel, EmailStr, Field


# Entrada do cadastro. Sem id (quem define é o banco).
# A senha chega em texto puro e o serviço guarda só o hash (seguranca.gerar_hash).
class UsuarioCriar(BaseModel):
    nome: str = Field(min_length=3, max_length=100)              # os mesmos tamanhos das colunas no banco
    email: EmailStr = Field(max_length=100)                      # EmailStr: só aceita um e-mail válido
    senha: str = Field(min_length=8, max_length=72)
    # Aula 10 · grupos: o tipo virou grupo. Chega o NOME do grupo, e o serviço busca o id.
    # Antes:  tipo: str = Field(default="solicitante", pattern="^(solicitante|executor)$")
    grupo: str = Field(default="solicitante", pattern="^(solicitante|executor)$")
    plano: str = Field(default="gratuito", pattern="^(gratuito|premium)$")


# Aula 10 · grupos: o grupo como sai na resposta, dentro do usuário.
# Sem as permissões: a API mostra a qual grupo a pessoa pertence, não a matriz de acesso.
class GrupoSaida(BaseModel):
    id: int
    nome: str


# Saída das rotas. Sem a senha: o hash nunca sai da API.
class UsuarioSaida(BaseModel):
    id: int
    nome: str
    email: str
    # Aula 10 · grupos: esquema dentro de esquema. O response_model lê usuario.grupo
    # (o relationship do modelo) e monta {"id": 1, "nome": "solicitante"}.
    # Antes:  tipo: str
    grupo: GrupoSaida
    plano: str


# Entrada do /login: só e-mail e senha, em JSON.
class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str


# Resposta do /login: o token e o tipo dele. Nunca inclui senha nem hash.
class Token(BaseModel):
    access_token: str
    token_type: str
