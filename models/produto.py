from extensions import db
from sqlalchemy import Numeric


class Produto(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_vestuario.id'), nullable=False)
    tipo = db.relationship('TipoVestuario', backref=db.backref('produtos', lazy='dynamic'))

    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=False)
    fabrica = db.relationship('Fabrica', backref=db.backref('produtos', lazy='dynamic'))

    tamanho_id = db.Column(db.Integer, db.ForeignKey('tamanho.id'), nullable=False)
    tamanho = db.relationship('Tamanho', backref=db.backref('produtos', lazy='dynamic'))

    cor_id = db.Column(db.Integer, db.ForeignKey('cor.id'), nullable=False)
    cor = db.relationship('Cor', backref=db.backref('produtos', lazy='dynamic'))

    status = db.Column(db.String(20), nullable=False, default="ativo")

    valor_compra = db.Column(Numeric(10, 2), nullable=False, default=0.0)
    valor_venda = db.Column(Numeric(10, 2), nullable=False, default=0.0)

    saldo_estoque = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return (f"<Produto {self.nome} | Tipo: {self.tipo.nome} | "
                f"Tamanho: {self.tamanho.descricao} | Cor: {self.cor.descricao}>")