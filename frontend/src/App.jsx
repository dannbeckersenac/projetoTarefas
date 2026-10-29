// Aula 9 · slides 26 e 27: o App guarda o token, descobre quem entrou e escolhe a tela do perfil.
// F12 > Application > Local Storage > http://localhost:5173: a chave "token" fica lá depois do login.
// F12 > Network: no "eu" e no "tarefas", veja o Request Header Authorization: Bearer eyJ...
import { useEffect, useState } from "react";
import Login from "./Login.jsx";
import ListaDeTarefas from "./ListaDeTarefas.jsx";
import Logo from "./Logo.jsx";
import { ENDERECO_API } from "./api.js";   // UC2 · o endereço da API vem do .env, não fica chumbado

// "Júlia Souza" → "JS": as iniciais que aparecem no avatar.
function iniciais(nome) {
  return nome
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((parte) => parte[0].toUpperCase())
    .join("");
}

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
  if (!usuario) {
    return (
      <div className="tela-carregando" role="status">
        <span className="girando" aria-hidden="true" />
        Carregando
      </div>
    );
  }

  // O executor vê a fila inteira; a solicitante vê só as dela.
  // Aula 10 · grupos: o /usuarios/eu não tem mais "tipo". Ele traz o grupo como objeto,
  // {"grupo": {"id": 2, "nome": "executor"}}, então a leitura é usuario.grupo.nome.
  // O filtro aqui só escolhe a tela: quem garante que a solicitante vê só as dela é a API.
  const executor = usuario.grupo.nome === "executor";
  const titulo = executor ? "Fila de tarefas" : "Minhas tarefas";
  const subtitulo = executor
    ? "Todos os pedidos do escritório, do mais novo ao mais antigo."
    : "Acompanhe o andamento dos pedidos que você abriu.";
  const filtro = executor ? "" : "solicitante_id=" + usuario.id;

  return (
    <div className="painel">
      <header className="topo">
        <div className="topo-conteudo">
          <Logo />
          <div className="topo-usuario">
            <div className="avatar" aria-hidden="true">{iniciais(usuario.nome)}</div>
            <div className="topo-identidade">
              <strong>{usuario.nome}</strong>
              {/* Aula 10 · grupos: o nome do grupo no lugar do antigo usuario.tipo */}
              <span>{usuario.grupo.nome}</span>
            </div>
            <button className="botao botao-fantasma" onClick={sair}>Sair</button>
          </div>
        </div>
      </header>

      <main className="conteudo">
        <ListaDeTarefas titulo={titulo} subtitulo={subtitulo} token={token} filtro={filtro} executor={executor} />
      </main>
    </div>
  );
}
