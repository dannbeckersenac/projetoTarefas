# Repositório de usuários: lista fixa, sem rota de cadastro (definido na cartilha).
# Continua em memória nesta etapa. Vai para o banco no segundo tempo da aula 6.
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
