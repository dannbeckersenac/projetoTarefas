// Uma tela protegida: todo fetch das rotas da cartilha leva o Authorization.
// Teste no F12 > Console: localStorage.setItem("token", "falso") e F5. O /usuarios/eu volta 401
// e o App manda de volta para o login.
import { useEffect, useState } from "react";
import { ENDERECO_API } from "./api.js";   // UC2 · o endereço da API vem do .env, não fica chumbado

export default function ListaDeTarefas({ titulo, token, filtro }) {
  const [tarefas, setTarefas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    // UC2 · antes: fetch("http://127.0.0.1:8000/tarefas"). Em produção, vira "/api/tarefas".
    fetch(ENDERECO_API + "/tarefas" + filtro, {
      headers: { Authorization: "Bearer " + token },
    })
      .then((resposta) => {
        if (!resposta.ok) throw new Error("não foi possível carregar as tarefas");
        return resposta.json();
      })
      .then((dados) => setTarefas(dados))
      .catch((problema) => setErro(problema.message))
      .finally(() => setCarregando(false));
  }, [token, filtro]);

  if (carregando) return <p>Carregando</p>;
  if (erro) return <p className="erro">{erro}</p>;

  return (
    <section>
      <h2>{titulo}</h2>
      {tarefas.length === 0 && <p>Nenhuma tarefa.</p>}
      <ul>
        {tarefas.map((tarefa) => (
          <li key={tarefa.id}>
            <strong>{tarefa.titulo}</strong> · {tarefa.situacao} · prazo {tarefa.prazo}
          </li>
        ))}
      </ul>
    </section>
  );
}
