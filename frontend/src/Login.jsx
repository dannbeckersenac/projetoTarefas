// Aula 9 · slide 25: a tela de login.
// F12 > Network: clique no "login" para ver o Payload (email e senha, em JSON)
// e a Response (access_token e token_type).
import { useState } from "react";
import { ENDERECO_API } from "./api.js";   // UC2 · o endereço da API vem do .env, não fica chumbado

export default function Login({ aoEntrar }) {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [mensagem, setMensagem] = useState("");

  function entrar(evento) {
    evento.preventDefault();   // o form não recarrega a página
    setMensagem("");
    // UC2 · antes: fetch("http://127.0.0.1:8000/login"). Em produção, vira "/api/login".
    fetch(ENDERECO_API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    })
      .then((resposta) => {
        if (!resposta.ok) throw new Error("e-mail ou senha incorretos");
        return resposta.json();
      })
      .then((dados) => {
        console.log("token recebido do /login:", dados.access_token);
        localStorage.setItem("token", dados.access_token);   // guarda a pulseira
        aoEntrar(dados.access_token);                        // avisa o App
      })
      .catch((problema) => setMensagem(problema.message));
  }

  return (
    <main className="cartao">
      <h1>Tarefa Certa</h1>
      <form onSubmit={entrar}>
        <label>
          E-mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Senha
          <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} required />
        </label>
        <button type="submit">Entrar</button>
      </form>
      {mensagem && <p className="erro">{mensagem}</p>}
    </main>
  );
}
