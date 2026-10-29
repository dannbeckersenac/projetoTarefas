// O endereço da API num lugar só. As telas importam daqui, em vez de escrever o endereço no fetch.
// import.meta.env é o jeito do Vite entregar ao código as variáveis do .env da pasta frontend/.
// O valor muda sozinho conforme o comando:
//   npm run dev   → .env.development → http://127.0.0.1:8000 (a API na minha máquina)
//   npm run build → .env.production  → /api (o navegador completa com o protocolo, o endereço
//                                          e a porta da própria tela; ver .docs/infra.md)
export const ENDERECO_API = import.meta.env.VITE_ENDERECO_API;
