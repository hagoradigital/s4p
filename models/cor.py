from extensions import db

class Cor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Cor {self.descricao}>"