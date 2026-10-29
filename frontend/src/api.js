// O endereço da API num lugar só. As telas importam daqui, em vez de escrever o endereço no fetch.
// import.meta.env é o jeito do Vite entregar ao código as variáveis do .env da pasta frontend/.
// O valor muda sozinho conforme o comando:
//   npm run dev   → .env.development → http://127.0.0.1:8000 (a API na minha máquina)
//   npm run build → .env.production  → /api (o navegador completa com o protocolo, o endereço
//                                          e a porta da própria tela; ver .docs/infra.md)
export const ENDERECO_API = import.meta.env.VITE_ENDERECO_API;

// Lê o "detail" que a API manda junto com o erro. Ele vem em dois formatos:
//   409/403/404 → {"detail": "Tarefa já concluída"}
//   422         → {"detail": [{"loc": ["body", "titulo"], "msg": "..."}, ...]}
export async function mensagemDeErro(resposta, padrao) {
  try {
    const dados = await resposta.json();
    if (typeof dados.detail === "string") return dados.detail;
    if (Array.isArray(dados.detail) && dados.detail.length > 0) {
      const primeiro = dados.detail[0];
      const campo = primeiro.loc ? primeiro.loc[primeiro.loc.length - 1] : "";
      return campo ? `${campo}: ${primeiro.msg}` : primeiro.msg;
    }
  } catch {
    // resposta sem JSON: fica a mensagem padrão
  }
  return padrao;
}
