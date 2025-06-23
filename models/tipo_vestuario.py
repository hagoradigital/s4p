from extensions import db

class TipoVestuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    fabrica_id = db.Column(db.Integer, db.ForeignKey('fabrica.id'), nullable=False)
    fabrica = db.relationship('Fabrica', backref=db.backref('tipos_vestuario', lazy=True))
    
    def __repr__(self):
        return f"<TipoVestuario {self.nome}>"