from extensions import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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