# Imagem base: Python 3.12 "slim", um Linux enxuto só com o necessário para rodar Python.
# Imagem menor baixa mais rápido e tem menos peças para dar problema.
FROM python:3.12-slim

# Pasta de trabalho dentro do contêiner. Os COPY e o CMD abaixo partem de /app.
WORKDIR /app

# Primeiro só a lista de dependências, e a instalação.
# Por quê: o Docker guarda cada etapa em cache. Enquanto o requirements.txt não mudar,
# o próximo build pula o pip install e reaproveita o que já foi baixado.
# --no-cache-dir: o pip não guarda os downloads dentro da imagem, que fica menor.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Depois o resto do código (main.py, rotas/, servicos/...). O .dockerignore deixa
# de fora o venv/, o .env e o __pycache__/. Mudar só o código refaz a partir daqui,
# sem reinstalar as dependências.
COPY . .

# O comando que roda quando o contêiner sobe. "fastapi run" é o modo de produção:
# sem recarga automática e ouvindo em 0.0.0.0, para o Caddy (outro contêiner) chegar.
# O main.py fica em /app/main.py, por isso o caminho é só "main.py".
CMD ["fastapi", "run", "main.py", "--port", "8000"]
