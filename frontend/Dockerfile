# Etapa 1, "build": uma máquina Node só para gerar os arquivos da tela.
# O AS build dá um nome a esta etapa, para a etapa 2 copiar coisas dela.
FROM node:22 AS build
WORKDIR /app

# Primeiro só o package.json e o package-lock.json, pelo mesmo motivo do backend:
# enquanto eles não mudarem, o cache pula o npm ci.
# npm ci instala exatamente as versões do package-lock.json, sem atualizar nada.
COPY package.json package-lock.json ./
RUN npm ci

# Depois o código da tela. O npm run build lê o .env.production (VITE_ENDERECO_API=/api)
# e gera HTML, JS e CSS prontos na pasta dist/.
COPY . .
RUN npm run build

# Etapa 2: a imagem final é só o Caddy com os arquivos prontos.
# O Node, o node_modules e o código-fonte ficam na etapa 1 e não entram aqui.
FROM caddy:2

# COPY --from=build pega o dist/ da etapa 1 e coloca em /srv,
# a pasta que o Caddyfile entrega com root * /srv e file_server.
COPY --from=build /app/dist /srv
