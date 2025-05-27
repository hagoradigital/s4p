from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class ClienteForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    endereco = StringField("Endereço", validators=[Optional()])
    numero = StringField("Número", validators=[Optional(), Length(max=10)])
    complemento = StringField("Complemento")
    cidade = StringField("Cidade", validators=[Optional()])
    uf = SelectField("UF", choices=[
        ("", "Selecione o estado"), ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"), ("BA", "BA"), ("CE", "CE"), 
        ("DF", "DF"), ("ES", "ES"), ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"), ("MG", "MG"), ("PA", "PA"), 
        ("PB", "PB"), ("PR", "PR"), ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"), ("RS", "RS"), ("RO", "RO"), 
        ("RR", "RR"), ("SC", "SC"), ("SP", "SP"), ("SE", "SE"), ("TO", "TO")
    ], validators=[Optional()])
    cep = StringField("CEP", validators=[Optional(), Length(min=8, max=10)])
    cnpj = StringField("CNPJ", validators=[Optional(), Length(min=14, max=18)])
    cpf = StringField("CPF do Responsável", validators=[Optional(), Length(min=11, max=14)])
    responsavel = StringField("Nome do Responsável", validators=[Optional()])
    celular = StringField("Celular", validators=[Optional()])
    telefone = StringField("Telefone")
    email = StringField("E-mail", validators=[Optional(), Email()])
    submit = SubmitField("Salvar")