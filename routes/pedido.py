from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Pedido, PedidoItem, Produto
from forms.pedido_form import PedidoForm, PedidoItemForm
from decimal import Decimal

pedido_bp = Blueprint("pedido", __name__)


# 🔸 Função para limpar máscara de moeda
def limpar_mascara_moeda(valor):
    if isinstance(valor, str):
        valor = valor.replace('.', '').replace(',', '.')
    try:
        return Decimal(valor) if valor else Decimal('0.00')
    except:
        return Decimal('0.00')


# 🔸 LISTAR PEDIDOS
@pedido_bp.route("/pedido", methods=["GET", "POST"])
@login_required
def pedido_listar():
    form = PedidoForm()
    form.carregar_clientes(current_user.fabrica_id)

    if request.method == "GET":
        form.cliente_id.data = 0
        form.valor_frete.data = "23,90"  # Valor default formatado para moeda BR

    if form.validate_on_submit():
        pedido = Pedido(
            cliente_id=form.cliente_id.data,
            valor_frete=limpar_mascara_moeda(form.valor_frete.data),
            status=form.status.data,
            fabrica_id=current_user.fabrica_id,
            usuario_id=current_user.id
        )
        pedido.gerar_numero()
        db.session.add(pedido)
        db.session.commit()
        flash("Pedido cadastrado com sucesso!", "success")
        return redirect(url_for("pedido.pedido_listar"))
    else:
        if request.method == "POST":
            flash("Erro ao registrar pedido. Verifique os campos.", "danger")
            return redirect(url_for("pedido.pedido_listar") + "#modalNovoPedido")

    pedidos = Pedido.query.filter_by(fabrica_id=current_user.fabrica_id).order_by(Pedido.data.desc()).all()

    valores_itens = {}
    for pedido in pedidos:
        total = sum(
            (item.quantidade or 0) * (item.produto.valor_venda or 0)
            for item in pedido.itens
        )
        valores_itens[pedido.id] = total

    formularios_edicao = {}
    for p in pedidos:
        form_edit = PedidoForm()
        form_edit.carregar_clientes(current_user.fabrica_id)
        form_edit.cliente_id.data = p.cliente_id
        form_edit.valor_frete.data = (
            f"{p.valor_frete:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            if p.valor_frete is not None else "0,00"
        )
        form_edit.status.data = p.status
        formularios_edicao[p.id] = form_edit

    conteudo = render_template(
        "admin/pedido_listar.html",
        pedidos=pedidos,
        valores_itens=valores_itens,
        form=form,
        formularios_edicao=formularios_edicao
    )

    return render_template(
        "dashboard.html",
        usuario=current_user,
        fabrica=current_user.fabrica,
        conteudo=conteudo
    )


# 🔸 EDITAR PEDIDO
@pedido_bp.route("/pedido/editar/<int:id>", methods=["POST"])
@login_required
def pedido_editar(id):
    pedido = Pedido.query.get_or_404(id)
    form = PedidoForm()
    form.carregar_clientes(current_user.fabrica_id)

    if form.validate_on_submit():
        pedido.cliente_id = form.cliente_id.data
        pedido.valor_frete = limpar_mascara_moeda(form.valor_frete.data)
        pedido.status = form.status.data
        db.session.commit()
        flash("Pedido atualizado com sucesso!", "success")
    else:
        flash("Erro ao atualizar pedido.", "danger")

    return redirect(url_for("pedido.pedido_listar"))


# 🔸 EXCLUIR PEDIDO
@pedido_bp.route("/pedido/excluir/<int:id>", methods=["POST"])
@login_required
def pedido_excluir(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    flash("Pedido excluído com sucesso!", "success")
    return redirect(url_for("pedido.pedido_listar"))


# 🔸 GERENCIAR ITENS DO PEDIDO
@pedido_bp.route("/pedido/itens/<int:pedido_id>", methods=["GET", "POST"])
@login_required
def pedido_itens(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    itens = PedidoItem.query.filter_by(pedido_id=pedido_id).all()

    form = PedidoItemForm()
    form.carregar_tipos_vestuario(current_user.fabrica_id)
    form.carregar_cores()

    tipo_id = request.form.get("tipo_id", type=int)
    cor_id = request.form.get("cor_id", type=int)

    if tipo_id and cor_id:
        form.carregar_produtos(current_user.fabrica_id, tipo_id, cor_id)

    if form.validate_on_submit():
        item = PedidoItem(
            pedido_id=pedido_id,
            produto_id=form.produto_id.data,
            quantidade=form.quantidade.data,
            informacao=form.informacao.data
        )
        db.session.add(item)
        db.session.commit()
        flash("Item adicionado com sucesso!", "success")
        return redirect(url_for('pedido.pedido_itens', pedido_id=pedido_id))

    conteudo = render_template(
        "admin/pedido_itens.html",
        pedido=pedido,
        itens=itens,
        form=form
    )

    return render_template(
        "dashboard.html",
        usuario=current_user,
        fabrica=current_user.fabrica,
        conteudo=conteudo
    )


# 🔸 EXCLUIR ITEM DO PEDIDO
@pedido_bp.route("/pedido/item/excluir/<int:id>", methods=["POST"])
@login_required
def pedido_item_excluir(id):
    item = PedidoItem.query.get_or_404(id)
    pedido_id = item.pedido_id
    db.session.delete(item)
    db.session.commit()
    flash("Item removido com sucesso!", "success")
    return redirect(url_for('pedido.pedido_itens', pedido_id=pedido_id))


# 🔸 API PARA BUSCAR PRODUTOS POR TIPO E COR
@pedido_bp.route("/api/produtos_por_tipo_e_cor/<int:tipo_id>/<int:cor_id>")
@login_required
def produtos_por_tipo_e_cor(tipo_id, cor_id):
    produtos = Produto.query.filter_by(
        fabrica_id=current_user.fabrica_id,
        tipo_id=tipo_id,
        cor_id=cor_id
    ).order_by(Produto.nome).all()

    return jsonify([
        {
            "id": p.id,
            "nome": f"{p.nome} → 🔸TAM: {p.tamanho.descricao} → COR: {p.cor.descricao}"
        } for p in produtos
    ])


# 🔸 VISUALIZAR PEDIDO (HTML PARA PDF)
@pedido_bp.route("/pedido/visualizar/<int:pedido_id>")
@login_required
def pedido_visualizar(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)

    total_itens = sum(
        Decimal(str(item.quantidade)) * Decimal(str(item.produto.valor_venda or '0'))
        for item in pedido.itens
    )

    frete = Decimal(str(pedido.valor_frete or '0'))
    total_geral = total_itens + frete

    return render_template(
        "admin/pedido_visualizar.html",
        pedido=pedido,
        total_itens=total_itens,
        total_geral=total_geral
    )