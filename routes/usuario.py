from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Usuario, Fabrica, RoleType
from forms.usuario_form import UsuarioForm
from sqlalchemy import or_, asc, desc

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

@usuario_bp.route("/usuario", methods=["GET", "POST"])
@login_required
def usuario_listar():
    if not current_user.is_authenticated or current_user.funcao not in ["master", "admin"]:
        flash("Acesso restrito.", "danger")
        return redirect(url_for("auth.dashboard"))

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    mostrar_modal = False
    form = UsuarioForm()
    form.fabrica_id.choices = [(f.id, f.nome) for f in Fabrica.query.all()]


    # Ajusta opções de função com base no tipo de usuário logado
    if not current_user.is_master():
        form.funcao.choices = [
            ("admin", "Admin da Fábrica"),
            ("medio", "Usuário Médio"),
            ("simples", "Usuário Simples")
        ]
    else:
        form.funcao.choices = [
            ("master", "Administrador Master"),
            ("admin", "Admin da Fábrica"),
            ("medio", "Usuário Médio"),
            ("simples", "Usuário Simples")
        ]
    

    if request.method == "POST":
        if form.validate_on_submit():
            novo_usuario = Usuario(
                nome=form.nome.data,
                email=form.email.data,
                funcao=form.funcao.data,
                ativo=form.ativo.data,
                fabrica_id=form.fabrica_id.data
            )
            novo_usuario.set_senha(form.senha.data)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("usuario.usuario_listar"))
        else:
            mostrar_modal = True

    query = Usuario.query

    # Se for admin de fábrica, filtra apenas os usuários da fábrica
    if current_user.funcao == "admin":
        query = query.filter_by(fabrica_id=current_user.fabrica_id)

    if search and len(search) >= 3:
        like = f"%{search}%"
        query = query.filter(
            or_(Usuario.nome.ilike(like), Usuario.email.ilike(like), Usuario.funcao.ilike(like))
        )

    coluna = getattr(Usuario, order_by, Usuario.nome)
    coluna = coluna.desc() if order_dir == "desc" else coluna.asc()
    usuarios = query.order_by(coluna).paginate(page=page, per_page=15)

    conteudo = render_template("admin/usuario_listar.html",
                               usuarios=usuarios,
                               form=form,
                               search=search,
                               order_by=order_by,
                               order_dir=order_dir,
                               mostrar_modal=mostrar_modal,
                               funcoes=[RoleType.MASTER, RoleType.ADMIN, RoleType.MEDIO, RoleType.SIMPLES],
                               fabricas=Fabrica.query.all())

    return render_template("dashboard.html",
                           usuario=current_user,
                           fabrica=current_user.fabrica,
                           total_clientes=0,
                           total_produtos=0,
                           total_pedidos_mes=0,
                           conteudo=conteudo)


@usuario_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar_usuario(id):
    if not current_user.is_authenticated or not current_user.is_master():
        flash("Acesso restrito ao administrador master.", "danger")
        return redirect(url_for("auth.dashboard"))

    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm()
    form.fabrica_id.choices = [(f.id, f.nome) for f in Fabrica.query.all()]


    # Ajusta opções de função com base no tipo de usuário logado
    if not current_user.is_master():
        form.funcao.choices = [
            ("admin", "Admin da Fábrica"),
            ("medio", "Usuário Médio"),
            ("simples", "Usuário Simples")
        ]
    else:
        form.funcao.choices = [
            ("master", "Administrador Master"),
            ("admin", "Admin da Fábrica"),
            ("medio", "Usuário Médio"),
            ("simples", "Usuário Simples")
        ]

    

    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.funcao = form.funcao.data
        usuario.ativo = form.ativo.data
        usuario.fabrica_id = form.fabrica_id.data

        if form.senha.data:
            usuario.set_senha(form.senha.data)

        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("usuario.usuario_listar"))

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    coluna = getattr(Usuario, order_by, Usuario.nome)
    coluna = coluna.desc() if order_dir == "desc" else coluna.asc()
    usuarios = Usuario.query.order_by(coluna).paginate(page=page, per_page=15)
    mostrar_modal = "editar"

    conteudo = render_template("admin/usuario_listar.html",
                               usuarios=usuarios,
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


@usuario_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_usuario(id):
    if not current_user.is_authenticated or not current_user.is_master():
        flash("Acesso restrito ao administrador master.", "danger")
        return redirect(url_for("auth.dashboard"))

    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído com sucesso!", "success")
    return redirect(url_for("usuario.usuario_listar"))