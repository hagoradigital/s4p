from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Estoque, Produto, TipoVestuario, Cor
from forms.estoque_form import EstoqueForm


estoque_bp = Blueprint("estoque", __name__)


# 🔸 LISTAR ESTOQUE
@estoque_bp.route("/estoque", methods=["GET"])
@login_required
def estoque_listar():
    form = EstoqueForm()
    form.carregar_tipos_vestuario()
    form.carregar_cores()

    page = request.args.get('page', 1, type=int)
    per_page = 10

    estoque = Estoque.query \
        .join(Produto) \
        .filter(Produto.fabrica_id == current_user.fabrica_id) \
        .order_by(Estoque.data_movimento.desc()) \
        .paginate(page=page, per_page=per_page)

    formularios_edicao = {}
    for mov in estoque.items:
        form_edit = EstoqueForm()
        form_edit.carregar_tipos_vestuario()
        form_edit.carregar_cores()

        if mov.produto and mov.produto.tipo_id:
            form_edit.tipo_id.data = mov.produto.tipo_id
            form_edit.cor_id.data = mov.produto.cor_id
            form_edit.carregar_produtos_por_tipo_e_cor(mov.produto.tipo_id, mov.produto.cor_id)
        else:
            form_edit.produto_id.choices = [(0, 'Selecione...')]

        form_edit.produto_id.data = mov.produto_id
        form_edit.quantidade.data = mov.quantidade
        form_edit.status_estoque.data = mov.status_estoque
        form_edit.valor_unitario.data = str(mov.valor_unitario).replace('.', ',') if mov.valor_unitario else ""
        form_edit.local_compra.data = mov.local_compra

        formularios_edicao[mov.id] = form_edit

    conteudo = render_template(
        "admin/estoque_listar.html",
        estoque=estoque,
        form=form,
        formularios_edicao=formularios_edicao
    )

    return render_template("dashboard.html",
                           usuario=current_user,
                           fabrica=current_user.fabrica,
                           conteudo=conteudo)


# 🔸 API PARA PRODUTOS POR TIPO E COR
@estoque_bp.route("/api/produtos_por_tipo_e_cor/<int:tipo_id>/<int:cor_id>")
@login_required
def produtos_por_tipo_e_cor(tipo_id, cor_id):
    produtos = Produto.query.filter_by(
        tipo_id=tipo_id,
        cor_id=cor_id,
        fabrica_id=current_user.fabrica_id
    ).all()

    return jsonify([{
        "id": p.id,
        "nome": f"{p.nome} → 🔸TAM: {p.tamanho.descricao} → COR: {p.cor.descricao}"
    } for p in produtos])


# 🔸 NOVO MOVIMENTO DE ESTOQUE
@estoque_bp.route("/estoque/novo", methods=["POST"])
@login_required
def estoque_novo():
    form = EstoqueForm()
    form.carregar_tipos_vestuario()
    form.carregar_cores()

    tipo_id = request.form.get("tipo_id", type=int)
    cor_id = request.form.get("cor_id", type=int)

    if tipo_id and cor_id:
        form.carregar_produtos_por_tipo_e_cor(tipo_id, cor_id)

    if form.validate_on_submit():
        try:
            valor_unitario_str = form.valor_unitario.data or "0"
            valor_unitario_float = float(valor_unitario_str.replace(".", "").replace(",", "."))

            movimento = Estoque(
                produto_id=form.produto_id.data,
                quantidade=form.quantidade.data,
                status_estoque=form.status_estoque.data,
                tipo_movimento="entrada",  # Sempre entrada no cadastro manual
                usuario_id=current_user.id,
                fabrica_id=current_user.fabrica_id,
                valor_unitario=valor_unitario_float,
                local_compra=form.local_compra.data
            )
            db.session.add(movimento)
            db.session.commit()

            flash("Movimento de estoque registrado com sucesso!", "success")
        except Exception as e:
            print("❌ Erro ao salvar:", e)
            flash("Erro ao registrar movimento.", "danger")

        return redirect(url_for("estoque.estoque_listar") + "#resetform")
    else:
        flash("Erro ao registrar movimento. Verifique os campos.", "danger")
        return redirect(url_for("estoque.estoque_listar") + "#resetform")


# 🔸 EXCLUIR MOVIMENTO
@estoque_bp.route("/estoque/excluir/<int:id>", methods=["POST"])
@login_required
def estoque_excluir(id):
    movimento = Estoque.query.get_or_404(id)
    db.session.delete(movimento)
    db.session.commit()
    flash("Movimento excluído com sucesso!", "success")
    return redirect(url_for("estoque.estoque_listar") + "#resetform")


# 🔸 EDITAR MOVIMENTO
@estoque_bp.route("/estoque/editar/<int:id>", methods=["POST"])
@login_required
def estoque_editar(id):
    movimento = Estoque.query.get_or_404(id)
    form = EstoqueForm()
    form.carregar_tipos_vestuario()
    form.carregar_cores()

    tipo_id = form.tipo_id.data
    cor_id = form.cor_id.data

    if tipo_id and cor_id:
        form.carregar_produtos_por_tipo_e_cor(tipo_id, cor_id)
    elif movimento.produto:
        form.carregar_produtos_por_tipo_e_cor(movimento.produto.tipo_id, movimento.produto.cor_id)

    if form.validate_on_submit():
        try:
            movimento.produto_id = form.produto_id.data
            movimento.quantidade = form.quantidade.data
            movimento.status_estoque = form.status_estoque.data
            movimento.valor_unitario = float(form.valor_unitario.data.replace(".", "").replace(",", ".")) if form.valor_unitario.data else None
            movimento.local_compra = form.local_compra.data

            db.session.commit()
            flash("Movimento de estoque atualizado com sucesso!", "success")
        except Exception as e:
            print("❌ Erro ao atualizar:", e)
            flash("Erro ao atualizar movimento.", "danger")

        return redirect(url_for("estoque.estoque_listar") + "#resetform")
    else:
        flash("Erro ao atualizar movimento. Verifique os campos.", "danger")
        return redirect(url_for("estoque.estoque_listar") + f"#modalEditarEstoque{id}")