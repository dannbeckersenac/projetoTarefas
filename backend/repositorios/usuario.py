# Repositório de usuários: lista fixa, sem rota de cadastro (definido na cartilha).
# Aula 6: a tabela usuarios existe no MySQL só para a ForeignKey da tarefa.
# A API continua consultando esta lista, por isso os ids daqui e da tabela precisam bater.
usuarios = [
    {"id": 1, "nome": "Júlia", "tipo": "solicitante"},
    {"id": 2, "nome": "Marcos", "tipo": "executor"},
    {"id": 3, "nome": "Paulo", "tipo": "solicitante"},
]


# Procura o usuário pelo id. Devolve None quando não existe, e quem decide o erro é a rota.
def buscar_por_id(usuario_id: int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    return None
