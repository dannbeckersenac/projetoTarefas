// O que a lista e o detalhe mostram igual: o nome da situação e o prazo com aviso.

export const ROTULO_SITUACAO = {
  aberta: "Aberta",
  "em andamento": "Em andamento",
  concluida: "Concluída",
};

// "em andamento" → "em-andamento": o nome vira parte da classe CSS (selo-em-andamento).
export function classeDaSituacao(situacao) {
  return situacao.replace(" ", "-");
}

// "2026-10-30" → "30 out". Monta a data pelas partes, sem fuso, para o dia não voltar um.
function formatarPrazo(prazo) {
  const [ano, mes, dia] = prazo.split("-").map(Number);
  const data = new Date(ano, mes - 1, dia);
  return data.toLocaleDateString("pt-BR", { day: "2-digit", month: "short" }).replace(".", "");
}

// Quantos dias faltam até o prazo (negativo se já passou).
function diasAte(prazo) {
  const [ano, mes, dia] = prazo.split("-").map(Number);
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  return Math.round((new Date(ano, mes - 1, dia) - hoje) / 86400000);
}

export function Prazo({ prazo, situacao }) {
  const dias = diasAte(prazo);
  let aviso = "";
  let classe = "";
  if (situacao !== "concluida") {
    if (dias < 0) { aviso = "atrasada"; classe = "prazo-atrasado"; }
    else if (dias === 0) { aviso = "vence hoje"; classe = "prazo-proximo"; }
    else if (dias <= 2) { aviso = dias === 1 ? "amanhã" : "em 2 dias"; classe = "prazo-proximo"; }
  }
  return (
    <span className={"prazo " + classe}>
      <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">
        <rect x="3" y="5" width="18" height="16" rx="3" fill="none" stroke="currentColor" strokeWidth="2" />
        <path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      </svg>
      {formatarPrazo(prazo)}
      {aviso && <em>· {aviso}</em>}
    </span>
  );
}
