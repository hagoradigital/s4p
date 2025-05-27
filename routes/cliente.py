# Rotas para CRUD de Clientes (routes/cliente.py)
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Cliente, Fabrica
from forms.cliente_form import ClienteForm
from sqlalchemy import or_, asc, desc

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

@cliente_bp.route("/cliente", methods=["GET", "POST"])
@login_required
def cliente_listar():
    form = ClienteForm()
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    mostrar_modal = False

    if request.method == "POST":
        if form.validate_on_submit():
            novo_cliente = Cliente(
                nome=form.nome.data,
                endereco=form.endereco.data,
                numero=form.numero.data,
                complemento=form.complemento.data,
                cidade=form.cidade.data,
                uf=form.uf.data,
                cep=form.cep.data,
                cnpj=form.cnpj.data,
                cpf=form.cpf.data,
                responsavel=form.responsavel.data,
                celular=form.celular.data,
                telefone=form.telefone.data,
                email=form.email.data,
                fabrica_id=current_user.fabrica_id
            )
            db.session.add(novo_cliente)
            db.session.commit()
            flash("Cliente cadastrado com sucesso!", "success")
            return redirect(url_for("cliente.cliente_listar"))
        else:
            mostrar_modal = True

    if current_user.is_master():
        query = Cliente.query  # mostra todos os clientes
    else:
        query = Cliente.query.filter_by(fabrica_id=current_user.fabrica_id)
    
    if search and len(search) >= 3:
        like_pattern = f"%{search}%"
        query = query.filter(or_(Cliente.nome.ilike(like_pattern), Cliente.email.ilike(like_pattern)))

    coluna = getattr(Cliente, order_by, Cliente.nome)
    coluna = coluna.desc() if order_dir == "desc" else coluna.asc()
    clientes = query.order_by(coluna).paginate(page=page, per_page=15)

    conteudo = render_template("admin/cliente_listar.html",
                               clientes=clientes,
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

@cliente_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm()

    if form.validate_on_submit():
        for campo in [
            "nome", "endereco", "numero", "complemento", "cidade", "uf", "cep", "cnpj",
            "responsavel", "cpf", "celular", "telefone", "email"]:
            setattr(cliente, campo, getattr(form, campo).data)

        db.session.commit()
        flash("Cliente atualizado com sucesso!", "success")
        return redirect(url_for("cliente.cliente_listar"))

@cliente_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente excluído com sucesso!", "success")
    return redirect(url_for("cliente.cliente_listar"))

@cliente_bp.route("/buscar_cep")
def buscar_cep():
    cep = request.args.get("cep")
    import requests
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"erro": "CEP não encontrado"}), 404