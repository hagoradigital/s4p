# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.10
FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

# Instala dependências de sistema mínimas
RUN apt-get update && apt-get install -y gcc libpq-dev

# Define diretório de trabalho
WORKDIR /code

# Copia as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Define a variável de ambiente padrão para produção
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Comando para iniciar o app
CMD ["flask", "run"]