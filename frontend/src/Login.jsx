// Aula 9 · slide 25: a tela de login.
// F12 > Network: clique no "login" para ver o Payload (email e senha, em JSON)
// e a Response (access_token e token_type).
import { useState } from "react";
import { ENDERECO_API } from "./api.js";   // UC2 · o endereço da API vem do .env, não fica chumbado
import Logo from "./Logo.jsx";

export default function Login({ aoEntrar }) {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [enviando, setEnviando] = useState(false);

  function entrar(evento) {
    evento.preventDefault();   // o form não recarrega a página
    setMensagem("");
    setEnviando(true);
    // UC2 · antes: fetch("http://127.0.0.1:8000/login"). Em produção, vira "/api/login".
    fetch(ENDERECO_API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    })
      .then((resposta) => {
        if (!resposta.ok) throw new Error("E-mail ou senha incorretos.");
        return resposta.json();
      })
      .then((dados) => {
        console.log("token recebido do /login:", dados.access_token);
        localStorage.setItem("token", dados.access_token);   // guarda a pulseira
        aoEntrar(dados.access_token);                        // avisa o App
      })
      .catch((problema) => setMensagem(problema.message))
      .finally(() => setEnviando(false));
  }

  return (
    <div className="login">
      <aside className="login-vitrine">
        <Logo tamanho={36} />
        <div>
          <h1>Cada pedido, do começo ao check final.</h1>
          <p>
            Abra pedidos internos, acompanhe o checklist de cada um e veja na hora o que já foi feito,
            sem precisar perguntar.
          </p>
        </div>
        <ul className="login-passos" aria-label="Como funciona">
          <li><span>1</span> Quem pede abre a tarefa</li>
          <li><span>2</span> Quem executa lança cada etapa</li>
          <li><span>3</span> A situação muda sozinha</li>
        </ul>
      </aside>

      <main className="login-area">
        <form className="login-cartao" onSubmit={entrar}>
          <div className="login-logo-celular"><Logo /></div>
          <h2>Entrar</h2>
          <p className="suave">Use o e-mail e a senha cadastrados no escritório.</p>

          <label className="campo">
            <span>E-mail</span>
            <input
              type="email"
              placeholder="voce@tarefacerta.com"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <label className="campo">
            <span>Senha</span>
            <input
              type="password"
              placeholder="••••••••"
              autoComplete="current-password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
          </label>

          {mensagem && <p className="alerta" role="alert">{mensagem}</p>}

          <button type="submit" className="botao botao-primario" disabled={enviando}>
            {enviando ? "Entrando…" : "Entrar"}
          </button>
        </form>
      </main>
    </div>
  );
}
