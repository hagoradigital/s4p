from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TipoVestuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    submit = SubmitField("Salvar")