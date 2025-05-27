from app import create_app
from extensions import db
from models import Pedido

app = create_app()

with app.app_context():
    Pedido.__table__.drop(db.engine, checkfirst=True)
    Pedido.__table__.create(db.engine, checkfirst=True)
    print("✅ Tabela Pedido atualizada com campo fabrica_id.")