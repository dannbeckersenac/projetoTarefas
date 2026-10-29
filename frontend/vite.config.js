import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Porta fixa: o ORIGEM_FRONTEND do backend/.env precisa ser exatamente http://localhost:5173.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true },
});
