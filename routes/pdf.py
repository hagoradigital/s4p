from flask import Blueprint, render_template, request, make_response
import pdfkit
import os

from models import Pedido
from extensions import db

pdf_bp = Blueprint("pdf", __name__)

# Caminho do binário do wkhtmltopdf no Replit
path_wkhtmltopdf = "/home/runner/workspace/wkhtmltox/usr/local/bin/wkhtmltopdf"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@pdf_bp.route("/pedido/pdf/<int:id>")
def gerar_pdf(id):
    pedido = Pedido.query.get_or_404(id)

    total_itens = sum(item.quantidade * item.produto.valor_venda for item in pedido.itens)
    total_geral = total_itens + (pedido.valor_frete or 0)

    # Adicionando variável 'ambiente' como 'producao' para controle no HTML
    rendered = render_template(
        "admin/pedido_visualizar.html",
        pedido=pedido,
        total_itens=total_itens,
        total_geral=total_geral,
        ambiente="producao"
    )

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=pedido_{pedido.numero}.pdf'
    return response