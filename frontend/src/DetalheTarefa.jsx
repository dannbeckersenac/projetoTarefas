// O detalhe de uma tarefa e o checklist dela.
//   GET  /tarefas/{id}        → a tarefa (os dois grupos, "tarefas:ver")
//   GET  /tarefas/{id}/itens  → os itens (os dois grupos, "itens:listar")
//   POST /tarefas/{id}/itens  → lança um item (só o executor, "itens:lancar")
// A regra fica na API: "etapa" soma 1 e põe em andamento, "conclusao" conclui,
// e tarefa concluída recusa item novo com 409. A tela só mostra o que a API devolve.
import { useCallback, useEffect, useState } from "react";
import { ENDERECO_API, mensagemDeErro } from "./api.js";
import Janela from "./Janela.jsx";
import { Prazo, ROTULO_SITUACAO, classeDaSituacao } from "./situacao.jsx";

function formatarData(data) {
  const [ano, mes, dia] = data.split("-").map(Number);
  return new Date(ano, mes - 1, dia).toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });
}

export default function DetalheTarefa({ tarefaId, token, executor, aoFechar, aoAlterar }) {
  const [tarefa, setTarefa] = useState(null);
  const [itens, setItens] = useState([]);
  const [erro, setErro] = useState("");

  const [tipo, setTipo] = useState("etapa");
  const [descricao, setDescricao] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [enviando, setEnviando] = useState(false);

  // As duas leituras saem juntas; a tela só aparece quando as duas voltam.
  const carregar = useCallback(async () => {
    const cabecalhos = { headers: { Authorization: "Bearer " + token } };
    try {
      const [respostaTarefa, respostaItens] = await Promise.all([
        fetch(ENDERECO_API + "/tarefas/" + tarefaId, cabecalhos),
        fetch(ENDERECO_API + "/tarefas/" + tarefaId + "/itens", cabecalhos),
      ]);
      if (!respostaTarefa.ok) throw new Error(await mensagemDeErro(respostaTarefa, "Tarefa não encontrada."));
      if (!respostaItens.ok) throw new Error(await mensagemDeErro(respostaItens, "Não foi possível ler o checklist."));
      setTarefa(await respostaTarefa.json());
      setItens(await respostaItens.json());
    } catch (problema) {
      setErro(problema.message);
    }
  }, [tarefaId, token]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function lancar(evento) {
    evento.preventDefault();
    setMensagem("");
    setEnviando(true);
    try {
      const resposta = await fetch(ENDERECO_API + "/tarefas/" + tarefaId + "/itens", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
        body: JSON.stringify({ tipo, descricao }),
      });
      if (!resposta.ok) throw new Error(await mensagemDeErro(resposta, "Não foi possível lançar o item."));
      setDescricao("");
      setTipo("etapa");
      await carregar();   // a situação e o contador mudaram na API: lê de novo
      aoAlterar();        // e a lista de trás também precisa ler
    } catch (problema) {
      setMensagem(problema.message);
    } finally {
      setEnviando(false);
    }
  }

  // Do mais antigo para o mais novo, como uma linha do tempo.
  const ordenados = [...itens].sort((a, b) => a.id - b.id);

  return (
    <Janela titulo="Detalhe da tarefa" aoFechar={aoFechar} lado="direita">
      {erro && <p className="alerta" role="alert">{erro}</p>}

      {!erro && !tarefa && (
        <div className="detalhe-carregando" role="status">
          <span className="girando" aria-hidden="true" /> Carregando
        </div>
      )}

      {tarefa && (
        <div className="detalhe">
          <div className="detalhe-cabecalho">
            <div className="tarefa-topo">
              <span className={"selo selo-" + classeDaSituacao(tarefa.situacao)}>
                {ROTULO_SITUACAO[tarefa.situacao] ?? tarefa.situacao}
              </span>
              <span className="tarefa-id">#{tarefa.id}</span>
            </div>
            <h2>{tarefa.titulo}</h2>
            {tarefa.descricao && <p className="detalhe-descricao">{tarefa.descricao}</p>}
          </div>

          <dl className="detalhe-dados">
            <div>
              <dt>Prazo</dt>
              <dd><Prazo prazo={tarefa.prazo} situacao={tarefa.situacao} /></dd>
            </div>
            <div>
              <dt>Etapas feitas</dt>
              <dd>{tarefa.itens_feitos}</dd>
            </div>
          </dl>

          <section>
            <h3 className="detalhe-titulo-secao">Checklist</h3>
            {ordenados.length === 0 ? (
              <p className="suave detalhe-vazio">
                Nenhum item lançado ainda.{executor ? "" : " Quem executa vai registrar cada etapa aqui."}
              </p>
            ) : (
              <ol className="linha-do-tempo">
                {ordenados.map((item) => (
                  <li key={item.id} className={"marco marco-" + item.tipo}>
                    <span className="marco-ponto" aria-hidden="true">
                      <svg width="12" height="12" viewBox="0 0 24 24">
                        <path d="M5 12.5l4 4L19 7" fill="none" stroke="currentColor" strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                    <div>
                      <strong>{item.descricao}</strong>
                      <span className="suave">
                        {item.tipo === "conclusao" ? "Conclusão" : "Etapa"} · {formatarData(item.data)}
                      </span>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </section>

          {executor && tarefa.situacao !== "concluida" && (
            <form className="lancar" onSubmit={lancar}>
              <h3 className="detalhe-titulo-secao">Lançar item</h3>
              <div className="alternador" role="radiogroup" aria-label="Tipo do item">
                <button
                  type="button"
                  role="radio"
                  aria-checked={tipo === "etapa"}
                  className={tipo === "etapa" ? "ativo" : ""}
                  onClick={() => setTipo("etapa")}
                >
                  Etapa
                </button>
                <button
                  type="button"
                  role="radio"
                  aria-checked={tipo === "conclusao"}
                  className={tipo === "conclusao" ? "ativo" : ""}
                  onClick={() => setTipo("conclusao")}
                >
                  Conclusão
                </button>
              </div>
              <p className="suave lancar-dica">
                {tipo === "etapa"
                  ? "Soma uma etapa feita e deixa a tarefa em andamento."
                  : "Encerra a tarefa. Depois disso, ela não recebe mais itens."}
              </p>
              <label className="campo">
                <span>Descrição</span>
                <input
                  value={descricao}
                  onChange={(e) => setDescricao(e.target.value)}
                  placeholder={tipo === "etapa" ? "Ex.: Orçamento aprovado" : "Ex.: Toner entregue na recepção"}
                  minLength={3}
                  maxLength={200}
                  required
                />
              </label>
              {mensagem && <p className="alerta" role="alert">{mensagem}</p>}
              <button type="submit" className="botao botao-primario" disabled={enviando}>
                {enviando ? "Lançando…" : tipo === "etapa" ? "Lançar etapa" : "Concluir tarefa"}
              </button>
            </form>
          )}

          {tarefa.situacao === "concluida" && (
            <p className="detalhe-concluida">
              <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M5 12.5l4 4L19 7" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              Tarefa concluída. O checklist está fechado.
            </p>
          )}
        </div>
      )}
    </Janela>
  );
}
