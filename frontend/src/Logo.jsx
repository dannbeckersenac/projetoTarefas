// O símbolo da Tarefa Certa: um check dentro de um quadrado arredondado.
// Usado no login e na barra do topo.
export default function Logo({ tamanho = 32 }) {
  return (
    <span className="logo">
      <svg width={tamanho} height={tamanho} viewBox="0 0 32 32" aria-hidden="true">
        <rect width="32" height="32" rx="9" fill="currentColor" />
        <path
          d="M9 16.5l4.5 4.5L23 11.5"
          fill="none"
          stroke="white"
          strokeWidth="3.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <span className="logo-nome">Tarefa Certa</span>
    </span>
  );
}
