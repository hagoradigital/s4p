import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "minha-chave-super-secreta")

    # Corrige URL de conexão se necessário
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Usa banco do Fly.io via proxy ou SQLite como fallback
    # SQLALCHEMY_DATABASE_URI = (database_url or "postgresql://postgres:6shoaqhogqTSj4c@localhost:5432/postgres")

    # Usa PostgreSQL se DATABASE_URL estiver definido, senão SQLite local
    SQLALCHEMY_DATABASE_URI = (database_url or "sqlite:///instance/sgp.db")


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "pt"