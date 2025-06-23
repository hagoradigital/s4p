from flask import Blueprint, render_template, request
from models import Cliente
from utils.token import gerar_token_cliente

gerar_link_bp = Blueprint('gerar_link', __name__)


@gerar_link_bp.route('/gerar_link', methods=['GET', 'POST'])
def gerar_link():
    link_gerado = None
    cliente_selecionado = None

    clientes = Cliente.query.order_by(Cliente.nome).all()

    if request.method == 'POST':
        cliente_id = int(request.form.get('cliente_id'))
        cliente_selecionado = Cliente.query.get_or_404(cliente_id)
        token = gerar_token_cliente(cliente_id)
        link_gerado = f"https://seusite.com/formulario_cliente/{token}"

    return render_template(
        'gerar_link.html',
        clientes=clientes,
        link_gerado=link_gerado,
        cliente=cliente_selecionado
    )