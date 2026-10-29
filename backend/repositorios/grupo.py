# Aula 10 · grupos: repositório de grupos. Só leitura: os grupos e as permissões
# nascem na migration criado_grupos_e_permissoes, e a API não cria nem altera grupo.
from sqlalchemy import select

from modelos.grupo import Grupo


# Aula 10 · grupos: SELECT de um grupo pelo nome ("solicitante" ou "executor").
# O cadastro recebe o nome do grupo e precisa do id para gravar em usuarios.grupo_id.
# Devolve None se não existir.
def buscar_por_nome(sessao, nome: str):
    consulta = select(Grupo).where(Grupo.nome == nome)
    return sessao.scalars(consulta).first()
