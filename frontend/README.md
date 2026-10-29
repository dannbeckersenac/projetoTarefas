# Frontend

React com Vite. A API precisa estar rodando em `http://127.0.0.1:8000`, e o `backend/.env`
precisa ter `ORIGEM_FRONTEND=http://localhost:5173`.

No PowerShell, na pasta `frontend`:

```powershell
npm install
npm run dev
```

Abra `http://localhost:5173`.

## Telas

- `src/Login.jsx`: envia e-mail e senha para o `POST /login` e guarda o token no `localStorage`.
- `src/App.jsx`: busca o `GET /usuarios/eu` com o token e escolhe a tela do perfil.
- `src/ListaDeTarefas.jsx`: lista as tarefas com o `Authorization: Bearer` no cabeçalho.
