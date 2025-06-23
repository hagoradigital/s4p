from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from models import TipoVestuario, Cor, Produto
from flask_login import current_user


class EstoqueForm(FlaskForm):
    tipo_id = SelectField(
        "Categoria",
        coerce=int,
        validators=[DataRequired(message="Selecione a categoria.")]
    )

    cor_id = SelectField(
        "Cor",
        coerce=int,
        validators=[DataRequired(message="Selecione a cor.")]
    )

    produto_id = SelectField(
        "Produto",
        coerce=int,
        validators=[DataRequired(message="Selecione o produto.")]
    )

    quantidade = IntegerField(
        "Quantidade",
        validators=[DataRequired(message="Informe a quantidade.")]
    )

    status_estoque = SelectField(
        "Status",
        choices=[
            ("Estoque", "Estoque"),
            ("Comprar", "Comprar"),
            ("Em Trânsito", "Em Trânsito")
        ],
        validators=[DataRequired(message="Selecione o status.")]
    )

    valor_unitario = StringField(
        "Valor Unitário"
    )

    local_compra = StringField(
        "Local da Compra"
    )

    submit = SubmitField("Salvar")

    # 🔸 Carregar categorias (tipos)
    def carregar_tipos_vestuario(self):
        tipos = TipoVestuario.query.filter_by(fabrica_id=current_user.fabrica_id).order_by(TipoVestuario.nome).all()
        self.tipo_id.choices = [(0, "Selecione...")] + [(t.id, t.nome) for t in tipos]

    # 🔸 Carregar cores
    def carregar_cores(self):
        cores = Cor.query.order_by(Cor.descricao).all()
        self.cor_id.choices = [(0, "Selecione...")] + [(c.id, c.descricao) for c in cores]

    # 🔸 Carregar produtos com filtro de tipo e cor
    def carregar_produtos_por_tipo_e_cor(self, tipo_id, cor_id):
        produtos = Produto.query.filter_by(
            tipo_id=tipo_id,
            cor_id=cor_id,
            fabrica_id=current_user.fabrica_id
        ).order_by(Produto.nome).all()

        self.produto_id.choices = (
            [(0, "Selecione...")] +
            [(p.id, f"{p.nome} → 🔸TAM: {p.tamanho.descricao} → COR: {p.cor.descricao}") for p in produtos]
        )

    # 🔥 Validações
    def validate_tipo_id(self, field):
        if field.data == 0:
            raise ValidationError("Selecione a categoria.")

    def validate_cor_id(self, field):
        if field.data == 0:
            raise ValidationError("Selecione a cor.")

    def validate_produto_id(self, field):
        if field.data == 0:
            raise ValidationError("Selecione o produto.")