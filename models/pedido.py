from extensions import db
from datetime import datetime


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=False)
    fabrica = db.relationship('Fabrica', backref=db.backref('pedidos', lazy=True))

    numero = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    valor_frete = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False)  # Ex.: Em Análise, Aprovado, Recusado

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relacionamentos
    cliente = db.relationship('Cliente', backref='pedidos')
    usuario = db.relationship('Usuario')
    itens = db.relationship('PedidoItem', backref='pedido', cascade="all, delete-orphan")

    def gerar_numero(self):
        ultimo_numero = db.session.query(db.func.max(Pedido.numero)).filter_by(fabrica_id=self.fabrica_id).scalar()
        self.numero = (ultimo_numero or 0) + 1

    def __repr__(self):
        return f"<Pedido {self.numero} - Cliente {self.cliente_id}>"


class PedidoItem(db.Model):
    __tablename__ = "pedido_item"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False)
    informacao = db.Column(db.String(100))

    # Relacionamentos
    produto = db.relationship('Produto')

    def __repr__(self):
        return f"<PedidoItem {self.id} - Pedido {self.pedido_id}>"