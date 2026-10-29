// Aula 9 · slides 26 e 27: o App guarda o token, descobre quem entrou e escolhe a tela do perfil.
// F12 > Application > Local Storage > http://localhost:5173: a chave "token" fica lá depois do login.
// F12 > Network: no "eu" e no "tarefas", veja o Request Header Authorization: Bearer eyJ...
import { useEffect, useState } from "react";
import Login from "./Login.jsx";
import ListaDeTarefas from "./ListaDeTarefas.jsx";
import { ENDERECO_API } from "./api.js";   // UC2 · o endereço da API vem do .env, não fica chumbado

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));   // sobrevive ao F5
  const [usuario, setUsuario] = useState(null);

  useEffect(() => {
    if (!token) return;                                 // sem pulseira, nada a buscar
    // UC2 · antes: fetch("http://127.0.0.1:8000/usuarios/eu"). Em produção, vira "/api/usuarios/eu".
    fetch(ENDERECO_API + "/usuarios/eu", {
      headers: { Authorization: "Bearer " + token },     // o que o /docs fazia
    })
      .then((resposta) => {
        if (!resposta.ok) throw new Error("pulseira vencida");
        return resposta.json();
      })
      .then((dados) => setUsuario(dados))
      .catch(() => { localStorage.removeItem("token"); setToken(null); });
  }, [token]);                                      // roda de novo se o token mudar

  function sair() {
    localStorage.removeItem("token");   // é assim que se faz o sair
    setToken(null);
    setUsuario(null);
  }

  if (!token) return <Login aoEntrar={setToken} />;
  if (!usuario) return <p className="cartao">Carregando</p>;

  // O executor vê a fila inteira; a solicitante vê só as dela.
  // Aula 10 · grupos: o /usuarios/eu não tem mais "tipo". Ele traz o grupo como objeto,
  // {"grupo": {"id": 2, "nome": "executor"}}, então a leitura é usuario.grupo.nome.
  // O filtro aqui só escolhe a tela: quem garante que a solicitante vê só as dela é a API.
  const titulo = usuario.grupo.nome === "executor" ? "Fila de tarefas" : "Minhas tarefas";
  const filtro = usuario.grupo.nome === "executor" ? "" : "?solicitante_id=" + usuario.id;

  return (
    <main className="cartao">
      <header>
        {/* Aula 10 · grupos: o nome do grupo no lugar do antigo usuario.tipo */}
        <span>Olá, {usuario.nome} ({usuario.grupo.nome})</span>
        <button onClick={sair}>Sair</button>
      </header>
      <ListaDeTarefas titulo={titulo} token={token} filtro={filtro} />
    </main>
  );
}
