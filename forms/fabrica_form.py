from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional
from wtforms import HiddenField

class FabricaForm(FlaskForm):
    id = HiddenField()  # novo campo oculto para guardar o ID
    nome = StringField("Nome", validators=[DataRequired()])
    cnpj = StringField("CNPJ", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])
    responsavel = StringField("Responsável", validators=[Optional()])
    celular = StringField("Celular", validators=[Optional()])
    status = SelectField("Status", choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")], validators=[Optional()])
    tipo = SelectField("Tipo de Fábrica", choices=[("Roupas", "Roupas"), ("Tecnologia", "Tecnologia")], validators=[Optional()])
    observacao = TextAreaField("Observação", validators=[Optional()])
    submit = SubmitField("Salvar")