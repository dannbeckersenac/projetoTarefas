// Abrir tarefa: POST /tarefas, só para o grupo solicitante ("tarefas:criar").
// O corpo leva título, descrição e prazo. O dono vem do token, e a situação
// (aberta) e o itens_feitos (0) quem define é o serviço.
import { useState } from "react";
import { ENDERECO_API, mensagemDeErro } from "./api.js";
import Janela from "./Janela.jsx";

// O dia de hoje no formato do input date (AAAA-MM-DD), no fuso de quem usa.
function hojeISO() {
  const hoje = new Date();
  hoje.setMinutes(hoje.getMinutes() - hoje.getTimezoneOffset());
  return hoje.toISOString().slice(0, 10);
}

export default function NovaTarefa({ token, aoFechar, aoCriar }) {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [prazo, setPrazo] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function criar(evento) {
    evento.preventDefault();
    setMensagem("");
    setEnviando(true);
    try {
      const resposta = await fetch(ENDERECO_API + "/tarefas", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
        body: JSON.stringify({ titulo, descricao, prazo }),
      });
      if (!resposta.ok) throw new Error(await mensagemDeErro(resposta, "Não foi possível abrir a tarefa."));
      aoCriar(await resposta.json());   // 201: a tarefa criada, já com o id do banco
    } catch (problema) {
      setMensagem(problema.message);
      setEnviando(false);
    }
  }

  return (
    <Janela titulo="Nova tarefa" aoFechar={aoFechar}>
      <form className="formulario" onSubmit={criar}>
        <div>
          <h2>Nova tarefa</h2>
          <p className="suave">Descreva o pedido. Quem executa vai lançar cada etapa no checklist.</p>
        </div>

        <label className="campo">
          <span>Título</span>
          <input
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            placeholder="Ex.: Comprar toner para a impressora"
            minLength={3}
            maxLength={100}
            required
            autoFocus
          />
        </label>

        <label className="campo">
          <span className="campo-rotulo">
            Descrição <small className="suave">{descricao.length}/500</small>
          </span>
          <textarea
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            placeholder="Detalhes que ajudam quem vai executar"
            maxLength={500}
            rows={4}
          />
        </label>

        <label className="campo">
          <span>Prazo</span>
          <input type="date" value={prazo} min={hojeISO()} onChange={(e) => setPrazo(e.target.value)} required />
        </label>

        {mensagem && <p className="alerta" role="alert">{mensagem}</p>}

        <div className="formulario-acoes">
          <button type="button" className="botao botao-fantasma" onClick={aoFechar}>Cancelar</button>
          <button type="submit" className="botao botao-primario" disabled={enviando}>
            {enviando ? "Abrindo…" : "Abrir tarefa"}
          </button>
        </div>
      </form>
    </Janela>
  );
}
