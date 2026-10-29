# Infraestrutura

Plano de como o Tarefa Certa sairia da máquina de desenvolvimento para produção.
**É uma proposta.** Nada aqui está publicado, e nenhum provedor ou ferramenta foi escolhido.

## 1. Arquitetura de produção (proposta)

```mermaid
flowchart LR
    nav[Navegador do usuário<br/>cliente: roda o React] -->|HTTPS 443| web[Servidor web<br/>entrega a tela e encaminha /api]
    web -->|HTTP 8000, só /api| api[API FastAPI]
    api -->|MySQL 3306| banco[(MySQL<br/>tarefa_certa)]
```

Para testar no mermaid.live, cole só o conteúdo do bloco, começando na linha `flowchart LR`.
As linhas de abertura (três crases e `mermaid`) e de fechamento (três crases) são do Markdown e não do Mermaid.

| Peça | Onde roda | Porta | Acesso |
|---|---|---|---|
| Navegador | Máquina do usuário (computador do executor, celular da solicitante) | Nenhuma: é cliente e inicia as conexões | Não recebe tráfego |
| Servidor web | Servidor | 443 | **Público**: é a única porta aberta para a internet |
| API FastAPI | Servidor | 8000 | Interno: só o servidor web chega até ela |
| MySQL | Servidor (na mesma máquina da API ou em outra; escolha em aberto) | 3306 | Interno: só a API chega até ele |

- Uma porta pública só: quem está de fora só fala com a recepção, e a API e o banco ficam escondidos atrás dela.
- Tela e API na mesma origem (`https://<domínio>`): o navegador vê um endereço só, e a tela chama a API por `/api/...`.
- Hoje as rotas da API não têm `/api` no caminho (`main.py` liga os routers sem prefixo). Por isso, o servidor web teria que retirar o `/api` antes de encaminhar para a API. ?
- Os dados do MySQL precisam de armazenamento próprio, que continue existindo quando o programa for reiniciado ou trocado.

## 2. Desenvolvimento e produção

| | Desenvolvimento (hoje, no projeto) | Produção (o que precisaria mudar) |
|---|---|---|
| **API** | `fastapi dev main.py` na minha máquina, em `127.0.0.1:8000`, com recarga automática | Roda no servidor, na 8000 interna, sem recarga automática e sem acesso público. O navegador chega nela por `/api` na 443 |
| **Tela** | Vite com `npm run dev` em `localhost:5173` (porta fixa em `vite.config.js`). Os `fetch` apontam para `http://127.0.0.1:8000` | Os arquivos da tela são entregues pelo servidor web na 443. Os `fetch` precisam usar o caminho `/api/...` da mesma origem |
| **Banco** | MySQL local na 3306, schema `tarefa_certa`; migrations aplicadas à mão com `alembic upgrade head` | MySQL no servidor, 3306 interna, com armazenamento próprio para os dados. As migrations precisam ser aplicadas antes de subir uma versão nova da API |
| **`.env`** | `backend/.env` na minha máquina, fora do Git (`.gitignore`), com `ORIGEM_FRONTEND`, `BANCO_*` e `CHAVE_DO_TOKEN` | Um `.env` próprio do servidor: outra `CHAVE_DO_TOKEN`, outro usuário e senha do banco, e um `BANCO_HOST` que aponta para o banco interno. Nunca copiado da minha máquina nem versionado |
| **CORS** | Necessário: a tela (`localhost:5173`) e a API (`127.0.0.1:8000`) são origens diferentes. `main.py` libera só a origem lida de `ORIGEM_FRONTEND` | Desnecessário entre tela e API, que ficam na mesma origem. Com `ORIGEM_FRONTEND` vazia, `main.py` não libera nenhuma outra origem |

## 3. O caminho do login

Em produção, pela proposta acima. O código de hoje usa `http://127.0.0.1:8000/login` no lugar de `/api/login`.

1. **Máquina do usuário.** O navegador abre `https://<domínio>/`. O DNS traduz o domínio no IP do servidor.
2. **Servidor.** O servidor web responde na 443 e entrega a tela (HTML, JS e CSS).
3. **Máquina do usuário.** O React desenha a tela de login (`Login.jsx`). O usuário digita e-mail e senha e clica em **Entrar**.
4. **Máquina do usuário.** A função `entrar` impede o recarregamento da página e faz `fetch` `POST /api/login` com `{email, senha}` em JSON, por HTTPS.
5. **Servidor.** O servidor web recebe na 443, vê o `/api` e encaminha para a API em `127.0.0.1:8000`, por HTTP interno. ?
6. **Servidor.** O FastAPI confere o corpo com `LoginEntrada` (`EmailStr`) e responde 422 se o formato estiver errado.
7. **Servidor.** `obter_sessao` abre a sessão. `servicos/usuario.autenticar` chama `repositorios/usuario.buscar_por_email`, que faz um `SELECT` no MySQL pela 3306.
8. **Servidor.** `seguranca.verificar_senha` compara a senha com o hash guardado. A senha em texto puro nunca é gravada.
9. **Servidor.** Com tudo certo, `seguranca.criar_token(usuario.id)` assina o JWT (HS256, vale 60 minutos) com a `CHAVE_DO_TOKEN` do `.env` do servidor. Se algo falhar, a resposta é 401 `E-mail ou senha incorretos`, a mesma para e-mail inexistente e para senha errada.
10. **Servidor → máquina do usuário.** A resposta `200 {access_token, token_type}` volta pela API e pelo servidor web, por HTTPS.
11. **Máquina do usuário.** `Login.jsx` grava o token no `localStorage` e avisa o `App`. O `App` faz `GET /api/usuarios/eu` com `Authorization: Bearer <token>` e escolhe a tela pelo grupo.

Observação: `Login.jsx:24` mostra o token no Console do navegador. Isso ajuda na aula, mas em produção expõe o token a quem olhar o Console.

## 4. O que está chumbado

Lista de onde aparecem `localhost` e `127.0.0.1`. Esta aula não corrige nada.

**Usados pelo navegador.** Aqui, `127.0.0.1` significa *a máquina do usuário*:

| Onde | Uso | Em produção |
|---|---|---|
| `frontend/src/Login.jsx:14` | `fetch` do `POST /login` | **Quebra**: o celular da solicitante procuraria a API nele mesmo. Precisa virar `/api/login` |
| `frontend/src/App.jsx:14` | `fetch` do `GET /usuarios/eu` | **Quebra**, pelo mesmo motivo. Precisa virar `/api/usuarios/eu` |
| `frontend/src/ListaDeTarefas.jsx:12` | `fetch` do `GET /tarefas` | **Quebra**, pelo mesmo motivo. Precisa virar `/api/tarefas` |
| `frontend/src/App.jsx:2` | Comentário: onde ver o `localStorage` no F12 em desenvolvimento | Não afeta: é só texto |
| `frontend/vite.config.js:4` | Comentário: liga a porta 5173 ao `ORIGEM_FRONTEND` | Não afeta: vale só para o Vite de desenvolvimento |

**Usados no servidor.** Aqui, `localhost` significa *a própria máquina onde a API roda*:

| Onde | Uso | Em produção |
|---|---|---|
| `backend/configuracao.py:14` | Comentário com o formato do endereço do banco. O endereço real é montado do `.env` (`BANCO_HOST`) | Não afeta: o código já lê do `.env` |
| `backend/alembic.ini:89` | Valor de exemplo do Alembic (`driver://user:pass@localhost/dbname`). `migracoes/env.py` usa o `engine` de `banco.py` | Não afeta o `alembic upgrade`. Só seria lido no modo offline do Alembic ? |

**Na documentação.** Descrevem o ambiente de desenvolvimento e estão corretos para ele: `README.md:16`, `frontend/README.md:3, 4 e 13`, `.docs/deploy.md:10` e `.docs/proximos-passos.md:5`.

O valor de `BANCO_HOST` no `.env` não foi lido. Pode ser `localhost`, o que em produção só funciona se o MySQL estiver na mesma máquina da API. ?
