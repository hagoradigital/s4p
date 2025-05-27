from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # usa a instância global

class RoleType:
    MASTER = "master"
    ADMIN = "admin"
    MEDIO = "medio"
    SIMPLES = "simples"

class Fabrica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    email = db.Column(db.String(120))
    responsavel = db.Column(db.String(100))
    celular = db.Column(db.String(20))
    status = db.Column(db.String(10), default="Ativo")  # Ativo ou Inativo
    tipo = db.Column(db.String(50))  # Roupas ou Tecnologia
    observacao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usuarios = db.relationship("Usuario", backref="fabrica", lazy=True)

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    funcao = db.Column(db.String(20), nullable=False, default=RoleType.SIMPLES)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    fabrica_id = db.Column(db.Integer, db.ForeignKey("fabrica.id"), nullable=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    def is_master(self):
        return self.funcao == RoleType.MASTER
    def is_admin_fabrica(self):
        return self.funcao == RoleType.ADMIN
    def __repr__(self):
        return f"<Usuario {self.nome}>"

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(150), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(100))
    cidade = db.Column(db.String(100), nullable=True)
    uf = db.Column(db.String(2), nullable=True)
    cep = db.Column(db.String(10), nullable=True)
    cnpj = db.Column(db.String(18), nullable=True)
    cpf = db.Column(db.String(14), nullable=True)
    responsavel = db.Column(db.String(100), nullable=True)
    celular = db.Column(db.String(20), nullable=True)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120), nullable=True)
    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=True)
    fabrica = db.relationship('Fabrica', backref=db.backref('clientes', lazy=True))

    def __repr__(self):
        return f"<Cliente {self.nome}>"


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=False)
    fabrica = db.relationship('Fabrica', backref=db.backref('produtos', lazy=True))



class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=False)
    fabrica = db.relationship('Fabrica', backref=db.backref('pedidos', lazy=True))
