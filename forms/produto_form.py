from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from models import TipoVestuario, Tamanho, Cor
from flask_login import current_user


class ProdutoForm(FlaskForm):
    nome = StringField(
        "Nome do Produto",
        validators=[DataRequired(message="Informe o nome do produto.")]
    )

    tipo_id = SelectField(
        "Categoria",
        coerce=int,
        validators=[DataRequired(message="Selecione a categoria.")]
    )

    tamanho_id = SelectField(
        "Tamanho",
        coerce=int,
        validators=[DataRequired(message="Selecione o tamanho.")]
    )

    cor_id = SelectField(
        "Cor",
        coerce=int,
        validators=[DataRequired(message="Selecione a cor.")]
    )

    descricao = TextAreaField(
        "Descrição",
        validators=[Optional()]
    )

    valor_compra = StringField(
        "Valor de Compra",
        validators=[DataRequired(message="Informe o valor de compra.")]
    )

    valor_venda = StringField(
        "Valor de Venda",
        validators=[DataRequired(message="Informe o valor de venda.")]
    )

    status = SelectField(
        "Status",
        choices=[
            ('ativo', "Ativo"),
            ('inativo', "Inativo")
        ],
        validators=[DataRequired(message="Selecione o status.")]
    )
    
    submit = SubmitField("Salvar")
    

    # 🔸 Carregar listas
    def carregar_tipos_vestuario(self):
        tipos = TipoVestuario.query.filter_by(fabrica_id=current_user.fabrica_id).order_by(TipoVestuario.nome).all()
        self.tipo_id.choices = [(0, "Selecione...")] + [(t.id, t.nome) for t in tipos]

    def carregar_tamanhos(self):
        tamanhos = Tamanho.query.order_by(Tamanho.descricao).all()
        self.tamanho_id.choices = [(0, "Selecione...")] + [(t.id, t.descricao) for t in tamanhos]

    def carregar_cores(self):
        cores = Cor.query.order_by(Cor.descricao).all()
        self.cor_id.choices = [(0, "Selecione...")] + [(c.id, c.descricao) for c in cores]
        

    # 🔥 Validações customizadas
    def validate_tipo_id(self, field):
        if field.data == 0:
            raise ValidationError("Selecione a categoria.")

    def validate_tamanho_id(self, field):
        if field.data == 0:
            raise ValidationError("Selecione o tamanho.")

    def validate_cor_id(self, field):
        if field.data == 0:
            raise ValidationError("Selecione a cor.")

    def validate_status(self, field):
        if field.data == 0:
            raise ValidationError("Selecione o status.")