// Uma janela por cima da tela: o fundo escurece e o Esc ou o clique fora fecham.
// lado="direita" vira um painel que desliza da lateral (usado no detalhe da tarefa).
import { useEffect } from "react";

export default function Janela({ titulo, aoFechar, lado, children }) {
  useEffect(() => {
    function teclou(evento) {
      if (evento.key === "Escape") aoFechar();
    }
    document.addEventListener("keydown", teclou);
    document.body.style.overflow = "hidden";   // a lista de trás não rola junto
    return () => {
      document.removeEventListener("keydown", teclou);
      document.body.style.overflow = "";
    };
  }, [aoFechar]);

  return (
    <div className="janela-fundo" onMouseDown={(e) => e.target === e.currentTarget && aoFechar()}>
      <div
        className={"janela" + (lado === "direita" ? " janela-lateral" : "")}
        role="dialog"
        aria-modal="true"
        aria-label={titulo}
      >
        <button className="janela-fechar" onClick={aoFechar} aria-label="Fechar">
          <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
          </svg>
        </button>
        {children}
      </div>
    </div>
  );
}
