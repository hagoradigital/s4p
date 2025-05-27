import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "minha-chave-super-secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sgp.db"  # Depois trocamos por PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "pt"
