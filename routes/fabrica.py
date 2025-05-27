from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from forms import FabricaForm
from models import Fabrica
from sqlalchemy import or_, asc, desc, func

fabrica_bp = Blueprint("fabrica", __name__, url_prefix="/fabrica")

# LISTAR FÁBRICAS (com paginação, ordenação e cadastro via modal)
@fabrica_bp.route("/fabrica", methods=["GET", "POST"])
@login_required
def fabrica_listar():
    if not current_user.is_authenticated or not current_user.is_master():
        flash("Acesso restrito ao administrador master.", "danger")
        return redirect(url_for("auth.dashboard"))

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    mostrar_modal = False
    form = FabricaForm()

    if request.method == "POST":
        if form.validate_on_submit():
            nova_fabrica = Fabrica(
                nome=form.nome.data,
                cnpj=form.cnpj.data,
                email=form.email.data,
                responsavel=form.responsavel.data,
                celular=form.celular.data,
                status=form.status.data,
                tipo=form.tipo.data,
                observacao=form.observacao.data,
            )
            db.session.add(nova_fabrica)
            db.session.commit()
            flash("Fábrica cadastrada com sucesso!", "success")
            return redirect(url_for("fabrica.fabrica_listar"))
        else:
            mostrar_modal = True

    query = Fabrica.query
    if search and len(search) >= 3:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Fabrica.nome.ilike(like_pattern),
                Fabrica.cnpj.ilike(like_pattern),
                Fabrica.email.ilike(like_pattern),
                Fabrica.responsavel.ilike(like_pattern),
                Fabrica.celular.ilike(like_pattern),
                Fabrica.status.ilike(like_pattern),
                Fabrica.tipo.ilike(like_pattern),
                Fabrica.observacao.ilike(like_pattern)
            )
        )

    coluna_raw = getattr(Fabrica, order_by, Fabrica.nome)
    coluna = func.lower(coluna_raw)
    coluna = coluna.desc() if order_dir == "desc" else coluna.asc()

    fabricas = query.order_by(coluna).paginate(page=page, per_page=15)

    conteudo = render_template("admin/fabrica_listar.html",
                               fabricas=fabricas,
                               form=form,
                               search=search,
                               order_by=order_by,
                               order_dir=order_dir,
                               mostrar_modal=mostrar_modal)
    return render_template("dashboard.html",
                           usuario=current_user,
                           fabrica=current_user.fabrica,
                           total_clientes=0,
                           total_produtos=0,
                           total_pedidos_mes=0,
                           conteudo=conteudo)

# EDITAR FÁBRICA
@fabrica_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar_fabrica(id):
    if not current_user.is_authenticated or not current_user.is_master():
        flash("Acesso restrito ao administrador master.", "danger")
        return redirect(url_for("auth.dashboard"))

    fabrica = Fabrica.query.get_or_404(id)
    form = FabricaForm()

    if form.validate_on_submit():
        fabrica.nome = form.nome.data
        fabrica.cnpj = form.cnpj.data
        fabrica.email = form.email.data
        fabrica.responsavel = form.responsavel.data
        fabrica.celular = form.celular.data
        fabrica.status = form.status.data
        fabrica.tipo = form.tipo.data
        fabrica.observacao = form.observacao.data
        db.session.commit()
        flash("Fábrica atualizada com sucesso!", "success")
        return redirect(url_for("fabrica.fabrica_listar"))

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    sort_column = getattr(Fabrica, order_by, Fabrica.nome)
    sort_order = asc(func.lower(sort_column)) if order_dir == "asc" else desc(func.lower(sort_column))

    fabricas = Fabrica.query.order_by(sort_order).paginate(page=page, per_page=15)
    mostrar_modal = "editar"

    conteudo = render_template("admin/fabrica_listar.html",
                               fabricas=fabricas,
                               form=form,
                               mostrar_modal=mostrar_modal,
                               id_edicao=id,
                               search=search,
                               order_by=order_by,
                               order_dir=order_dir)
    return render_template("dashboard.html",
                           usuario=current_user,
                           fabrica=current_user.fabrica,
                           total_clientes=0,
                           total_produtos=0,
                           total_pedidos_mes=0,
                           conteudo=conteudo)

# EXCLUIR FÁBRICA
@fabrica_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_fabrica(id):
    if not current_user.is_authenticated or not current_user.is_master():
        flash("Acesso restrito ao administrador master.", "danger")
        return redirect(url_for("auth.dashboard"))

    fabrica = Fabrica.query.get_or_404(id)

    if fabrica.usuarios:
        return redirect(url_for("fabrica.fabrica_listar",
                                erro="nao_pode_excluir",
                                nome=fabrica.nome))

    db.session.delete(fabrica)
    db.session.commit()
    flash("Fábrica excluída com sucesso!", "success")
    return redirect(url_for("fabrica.fabrica_listar"))