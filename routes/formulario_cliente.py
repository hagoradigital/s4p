from flask import Blueprint, render_template, request, abort
from extensions import db
from models import Cliente
from forms.formulario_cliente_form import FormularioClienteForm
from utils.token import validar_token_cliente

formulario_cliente_bp = Blueprint("formulario_cliente", __name__)


@formulario_cliente_bp.route('/formulario_cliente/<token>', methods=['GET', 'POST'])
def formulario_cliente(token):
    cliente_id = validar_token_cliente(token)

    if cliente_id is None:
        abort(404)  # Token inválido ou expirado

    cliente = Cliente.query.get_or_404(cliente_id)
    form = FormularioClienteForm()

    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.telefone = form.telefone.data
        cliente.email = form.email.data
        cliente.endereco = form.endereco.data
        db.session.commit()
        return render_template('formulario_sucesso.html', cliente=cliente)

    if request.method == 'GET':
        form.nome.data = cliente.nome
        form.telefone.data = cliente.telefone
        form.email.data = cliente.email
        form.endereco.data = cliente.endereco

    return render_template('formulario_cliente.html', form=form, cliente=cliente)