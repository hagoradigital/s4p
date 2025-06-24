import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "minha-chave-super-secreta"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///instance/sgp.db"
    ).replace("postgres://", "postgresql://")  # 🔥 Ajuste para compatibilidade no Render

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = "pt"