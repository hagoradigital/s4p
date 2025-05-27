from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

class UsuarioForm(FlaskForm):
    id = HiddenField()
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    funcao = SelectField("Função", choices=[
        ("master", "Administrador Master"),
        ("admin", "Admin da Fábrica"),
        ("medio", "Usuário Médio"),
        ("simples", "Usuário Simples")
    ], validators=[DataRequired()])
    fabrica_id = SelectField("Fábrica", coerce=int, validators=[DataRequired()])
    ativo = BooleanField("Ativo", default=True)

    senha = PasswordField("Senha", validators=[Optional(), Length(min=6)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[Optional(), EqualTo('senha', message="As senhas não coincidem.")])

    submit = SubmitField("Salvar")

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False
    
        if not self.id.data:  # Cadastro
            if not self.senha.data:
                self.senha.errors.append("Campo obrigatório.")
                return False
            if not self.confirmar_senha.data:
                self.confirmar_senha.errors.append("Campo obrigatório.")
                return False
            if self.senha.data != self.confirmar_senha.data:
                self.confirmar_senha.errors.append("As senhas não conferem.")
                return False
    
        return True