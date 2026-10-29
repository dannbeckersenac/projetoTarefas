// Uma tela protegida: todo fetch das rotas da cartilha leva o Authorization.
// Teste no F12 > Console: localStorage.setItem("token", "falso") e F5. O /usuarios/eu volta 401
// e o App manda de volta para o login.
import { useEffect, useState } from "react";
import { ENDERECO_API } from "./api.js";   // UC2 · o endereço da API vem do .env, não fica chumbado
import DetalheTarefa from "./DetalheTarefa.jsx";
import NovaTarefa from "./NovaTarefa.jsx";
import { Prazo, ROTULO_SITUACAO, classeDaSituacao } from "./situacao.jsx";

// As abas do filtro. O valor vai no ?situacao= do GET /tarefas: quem filtra é o banco.
const SITUACOES = [
  { valor: "", rotulo: "Todas" },
  { valor: "aberta", rotulo: "Abertas" },
  { valor: "em andamento", rotulo: "Em andamento" },
  { valor: "concluida", rotulo: "Concluídas" },
];

// A API pagina de 10 em 10 (repositorios/tarefa.py). Página cheia = pode haver mais.
const POR_PAGINA = 10;

export default function ListaDeTarefas({ titulo, subtitulo, token, filtro, executor }) {
  const [tarefas, setTarefas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [situacao, setSituacao] = useState("");
  const [pagina, setPagina] = useState(1);
  const [versao, setVersao] = useState(0);              // muda quando algo foi gravado: lê de novo
  const [criando, setCriando] = useState(false);        // a janela de nova tarefa está aberta?
  const [tarefaAberta, setTarefaAberta] = useState(null);   // o id da tarefa no painel de detalhe

  useEffect(() => {
    setCarregando(true);
    setErro("");
    // Monta a query só com o que tem valor: ?pagina=1&solicitante_id=3&situacao=aberta
    const parametros = new URLSearchParams(filtro);
    parametros.set("pagina", pagina);
    if (situacao) parametros.set("situacao", situacao);
    // UC2 · antes: fetch("http://127.0.0.1:8000/tarefas"). Em produção, vira "/api/tarefas".
    fetch(ENDERECO_API + "/tarefas?" + parametros, {
      headers: { Authorization: "Bearer " + token },
    })
      .then((resposta) => {
        if (!resposta.ok) throw new Error("Não foi possível carregar as tarefas.");
        return resposta.json();
      })
      .then((dados) => setTarefas(dados))
      .catch((problema) => setErro(problema.message))
      .finally(() => setCarregando(false));
  }, [token, filtro, situacao, pagina, versao]);

  function trocarSituacao(valor) {
    setSituacao(valor);
    setPagina(1);   // filtro novo começa da primeira página
  }

  // A tarefa nova nasce aberta: volta para "Todas", página 1, e já abre o detalhe dela.
  function tarefaCriada(tarefa) {
    setCriando(false);
    setSituacao("");
    setPagina(1);
    setVersao((v) => v + 1);
    setTarefaAberta(tarefa.id);
  }

  return (
    <section>
      <div className="cabecalho">
        <div>
          <h1>{titulo}</h1>
          <p className="suave">{subtitulo}</p>
        </div>
        {/* Só o grupo solicitante tem "tarefas:criar". Se o botão aparecesse para o
            executor, a API devolveria 403: a tela só evita o clique inútil. */}
        {!executor && (
          <button className="botao botao-primario botao-icone" onClick={() => setCriando(true)}>
            <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" />
            </svg>
            Nova tarefa
          </button>
        )}
      </div>

      <div className="abas" role="tablist" aria-label="Filtrar por situação">
        {SITUACOES.map((opcao) => (
          <button
            key={opcao.valor}
            role="tab"
            aria-selected={situacao === opcao.valor}
            className={"aba" + (situacao === opcao.valor ? " aba-ativa" : "")}
            onClick={() => trocarSituacao(opcao.valor)}
          >
            {opcao.valor && <span className={"ponto ponto-" + classeDaSituacao(opcao.valor)} />}
            {opcao.rotulo}
          </button>
        ))}
      </div>

      {erro && <p className="alerta" role="alert">{erro}</p>}

      {carregando && (
        <ul className="grade" aria-busy="true">
          {[1, 2, 3].map((n) => <li key={n} className="tarefa esqueleto" />)}
        </ul>
      )}

      {!carregando && !erro && tarefas.length === 0 && (
        <div className="vazio">
          <svg width="48" height="48" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="4" y="3" width="16" height="18" rx="3" fill="none" stroke="currentColor" strokeWidth="1.6" />
            <path d="M8.5 12l2.5 2.5 4.5-5" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <strong>Nenhuma tarefa por aqui</strong>
          <span className="suave">
            {situacao ? "Nenhuma tarefa nesta situação." : "Quando um pedido for aberto, ele aparece nesta lista."}
          </span>
          {!executor && !situacao && (
            <button className="botao botao-primario" onClick={() => setCriando(true)}>Abrir a primeira tarefa</button>
          )}
        </div>
      )}

      {!carregando && !erro && tarefas.length > 0 && (
        <ul className="grade">
          {tarefas.map((tarefa) => (
            <li key={tarefa.id}>
              <button
                className={"tarefa tarefa-" + classeDaSituacao(tarefa.situacao)}
                onClick={() => setTarefaAberta(tarefa.id)}
              >
                <span className="tarefa-topo">
                  <span className={"selo selo-" + classeDaSituacao(tarefa.situacao)}>
                    {ROTULO_SITUACAO[tarefa.situacao] ?? tarefa.situacao}
                  </span>
                  <span className="tarefa-id">#{tarefa.id}</span>
                </span>
                <span className="tarefa-titulo">{tarefa.titulo}</span>
                {tarefa.descricao && <span className="tarefa-descricao">{tarefa.descricao}</span>}
                <span className="tarefa-rodape">
                  <Prazo prazo={tarefa.prazo} situacao={tarefa.situacao} />
                  <span className="etapas">
                    <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M5 12.5l4 4L19 7" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    {tarefa.itens_feitos} {tarefa.itens_feitos === 1 ? "etapa" : "etapas"}
                  </span>
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {!carregando && !erro && (pagina > 1 || tarefas.length === POR_PAGINA) && (
        <nav className="paginacao" aria-label="Páginas">
          <button className="botao botao-fantasma" disabled={pagina === 1} onClick={() => setPagina(pagina - 1)}>
            ← Anterior
          </button>
          <span className="suave">Página {pagina}</span>
          <button
            className="botao botao-fantasma"
            disabled={tarefas.length < POR_PAGINA}
            onClick={() => setPagina(pagina + 1)}
          >
            Próxima →
          </button>
        </nav>
      )}

      {criando && <NovaTarefa token={token} aoFechar={() => setCriando(false)} aoCriar={tarefaCriada} />}

      {tarefaAberta && (
        <DetalheTarefa
          tarefaId={tarefaAberta}
          token={token}
          executor={executor}
          aoFechar={() => setTarefaAberta(null)}
          aoAlterar={() => setVersao((v) => v + 1)}
        />
      )}
    </section>
  );
}
