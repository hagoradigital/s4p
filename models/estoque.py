from extensions import db
from datetime import datetime


class Estoque(db.Model):
    __tablename__ = "estoque"

    id = db.Column(db.Integer, primary_key=True)

    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=False)
    fabrica = db.relationship('Fabrica', backref=db.backref('estoque_movimentos', lazy=True))

    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    produto = db.relationship("Produto", backref="movimentos")

    quantidade = db.Column(db.Integer, nullable=False)
    tipo_movimento = db.Column(db.String(10), nullable=False)  # 'entrada' ou 'saida'
    status_estoque = db.Column(db.String(20), nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="movimentos")

    data_movimento = db.Column(db.DateTime, default=datetime.utcnow)

    referencia_entrada_id = db.Column(db.Integer, nullable=True)  # Para vincular uma saída a uma entrada (se necessário)

    valor_unitario = db.Column(db.Float)
    local_compra = db.Column(db.Text)

    def __repr__(self):
        return (f"<Estoque ID {self.id} | Produto {self.produto.nome} | "
                f"Quantidade {self.quantidade} | Tipo {self.tipo_movimento}>")