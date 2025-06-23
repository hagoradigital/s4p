from extensions import db
from datetime import datetime

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

    def __repr__(self):
        return f"<Fabrica {self.nome}>"