from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class RoleType:
    MASTER = "master"
    ADMIN = "admin"
    MEDIO = "medio"
    SIMPLES = "simples"


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)  # 🔥 aumentei para 256 para garantir espaço suficiente
    funcao = db.Column(db.String(20), nullable=False, default=RoleType.SIMPLES)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    fabrica_id = db.Column(db.Integer, db.ForeignKey("fabrica.id"), nullable=True)

    def set_senha(self, senha):
        # 🔥 Força o uso do algoritmo pbkdf2, que é seguro e compatível
        self.senha_hash = generate_password_hash(senha, method="pbkdf2:sha256")

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def is_master(self):
        return self.funcao == RoleType.MASTER

    def is_admin_fabrica(self):
        return self.funcao == RoleType.ADMIN

    def __repr__(self):
        return f"<Usuario {self.nome}>"