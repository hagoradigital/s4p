from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from models import Cliente, Produto, TipoVestuario, Cor


# 🔸 Validador para impedir seleção inválida (valor 0)
def validar_selecao(form, field):
    if field.data is None or field.data == 0:
        raise ValidationError('Selecione um cliente válido.')


class PedidoForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[validar_selecao])
    valor_frete = StringField('Valor do Frete', validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[
            ('Em Análise', 'Em Análise'),
            ('Aprovado', 'Aprovado'),
            ('Recusado', 'Recusado')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Salvar')

    def carregar_clientes(self, fabrica_id):
        clientes = Cliente.query.filter_by(fabrica_id=fabrica_id).order_by(Cliente.nome).all()
        self.cliente_id.choices = [(0, "Selecione o Cliente")] + [(c.id, c.nome) for c in clientes]


class PedidoItemForm(FlaskForm):
    tipo_id = SelectField('Categoria', coerce=int, validators=[validar_selecao])
    cor_id = SelectField('Cor', coerce=int, validators=[validar_selecao])
    produto_id = SelectField('Produto', coerce=int, validators=[validar_selecao])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    informacao = StringField('Informação')
    submit = SubmitField('Adicionar')

    def carregar_tipos_vestuario(self, fabrica_id):
        tipos = TipoVestuario.query.filter_by(fabrica_id=fabrica_id).order_by(TipoVestuario.nome).all()
        self.tipo_id.choices = [(0, "Selecione...")] + [(t.id, t.nome) for t in tipos]

    def carregar_cores(self):
        cores = Cor.query.order_by(Cor.descricao).all()
        self.cor_id.choices = [(0, "Selecione...")] + [(c.id, c.descricao) for c in cores]

    def carregar_produtos(self, fabrica_id, tipo_id=None, cor_id=None):
        query = Produto.query.filter_by(fabrica_id=fabrica_id)
        if tipo_id:
            query = query.filter_by(tipo_id=tipo_id)
        if cor_id:
            query = query.filter_by(cor_id=cor_id)

        produtos = query.order_by(Produto.nome).all()

        self.produto_id.choices = [(0, "Selecione...")] + [
            (p.id, f"{p.nome} → 🔸TAM: {p.tamanho.descricao} → COR: {p.cor.descricao}")
            for p in produtos
        ]