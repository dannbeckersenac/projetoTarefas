# 003 — Criar rota de login com JWT

Agente: Executor.

## Objetivo

Adicionar autenticação por e-mail e senha usando a configuração JWT já existente em `backend/seguranca.py`. O login valida a senha armazenada pelo cadastro e devolve um token Bearer assinado com `seguranca.criar_token(usuario.id)`.

## Arquivos que PODE editar

- `backend/rotas/autenticacao.py` → implementar `POST /autenticacao/login` e converter falha de credenciais em HTTP 401.
- `backend/main.py` → importar e registrar o router de autenticação.
- `backend/servicos/usuario.py` → localizar o usuário pelo e-mail e verificar a senha com `seguranca.verificar_senha`; em sucesso, gerar token com `seguranca.criar_token`.
- `backend/repositorios/usuario.py` → manter ou acrescentar a busca por e-mail utilizada pelo serviço.
- `backend/esquemas/usuario.py` → definir os esquemas de entrada e saída do login.

Não editar outros arquivos.

## Contrato (não pode mudar)

- Endpoint: `POST /autenticacao/login`.
- Entrada JSON: `{"email": "...", "senha": "..."}`. O e-mail é validado como `EmailStr`; a senha é obrigatória.
- Resposta HTTP 200: `{"access_token": "<JWT>", "token_type": "bearer"}`.
- Credenciais inválidas (e-mail inexistente ou senha incorreta): HTTP 401, detalhe `E-mail ou senha inválidos`, cabeçalho `WWW-Authenticate: Bearer`.
- O JWT é criado exclusivamente por `seguranca.criar_token(usuario.id)`. O prazo e o algoritmo permanecem os definidos em `seguranca.py`.
- A comparação da senha é feita exclusivamente por `seguranca.verificar_senha`; não comparar texto puro nem expor o hash.
- A rota usa `Depends(obter_sessao)` e segue o fluxo rota → serviço → repositório.
- Não alterar as regras de cadastro nem os contratos existentes de usuários.

## Passo a passo

1. Criar os esquemas de entrada e resposta do login em `esquemas/usuario.py`.
2. Implementar no serviço a busca do usuário pelo e-mail, validação do hash e criação do token. Para qualquer credencial inválida, retornar um resultado de falha sem revelar se o e-mail existe.
3. Implementar o router com prefixo `/autenticacao`, rota `POST /login`, dependência da sessão e resposta 401 conforme o contrato.
4. Registrar o router em `main.py`.
5. Revisar as alterações para confirmar que apenas os cinco arquivos listados foram editados e que nenhum segredo ou hash aparece na resposta.

## Exemplos

- E-mail existente e senha correta → HTTP 200 com token JWT e `token_type` igual a `bearer`.
- E-mail inexistente → HTTP 401 com a mensagem uniforme de credenciais inválidas.
- E-mail existente e senha incorreta → mesma resposta HTTP 401 do e-mail inexistente.

## Pronto quando

- O endpoint consta na documentação OpenAPI em `/docs` como `POST /autenticacao/login`.
- A resposta de sucesso contém somente os campos `access_token` e `token_type`.
- Credenciais inválidas recebem HTTP 401 e `WWW-Authenticate: Bearer`.
- A implementação usa as funções de hash/JWT existentes e não altera `seguranca.py`.
- A revisão confirma que nenhum arquivo fora da lista permitida foi editado.

## Verificação manual sugerida

1. Cadastrar um usuário com `POST /usuarios`.
2. Enviar `POST /autenticacao/login` com o e-mail e a senha cadastrados; conferir HTTP 200 e um token.
3. Repetir com senha incorreta e com e-mail inexistente; conferir HTTP 401 uniforme.

## Proibido nesta tarefa

- Alterar `backend/seguranca.py`, `.env`, banco de dados, migrações, frontend ou testes.
- Criar dependências, arquivos ou endpoints adicionais.
- Retornar senha, hash, dados pessoais do usuário ou detalhes que revelem se o e-mail está cadastrado.
- Implementar recuperação de senha, refresh token, logout ou dependência para proteger outras rotas.
