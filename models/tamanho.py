from extensions import db

class Tamanho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<Tamanho {self.descricao}>"