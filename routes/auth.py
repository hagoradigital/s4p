from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import Usuario, Cliente, Produto, Pedido
from forms import LoginForm
from datetime import datetime
from extensions import db, login_manager

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    form = LoginForm()
    return render_template("index.html", form=form)

@auth_bp.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_senha(form.password.data):
            login_user(usuario, remember=form.remember_me.data)
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Email ou senha inválidos", "danger")
    return render_template("index.html", form=form)


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    usuario = current_user
    fabrica = usuario.fabrica

    total_clientes = 0
    total_produtos = 0
    total_pedidos_mes = 0

    if fabrica:
        total_clientes = Cliente.query.filter_by(fabrica_id=fabrica.id).count()
        total_produtos = Produto.query.filter_by(fabrica_id=fabrica.id).count()

        now = datetime.utcnow()
        total_pedidos_mes = Pedido.query.filter(
            Pedido.fabrica_id == fabrica.id,
            Pedido.data >= datetime(now.year, now.month, 1)
        ).count()

    return render_template(
        "dashboard.html",
        usuario=usuario,
        fabrica=fabrica,
        total_clientes=total_clientes,
        total_produtos=total_produtos,
        total_pedidos_mes=total_pedidos_mes
    )
    
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.index"))

@auth_bp.route("/debug")
@login_required
def debug():
    usuario = current_user
    return f"""
    <h3>DEBUG USUÁRIO</h3>
    Nome: {usuario.nome}<br>
    Email: {usuario.email}<br>
    Fábrica ID: {usuario.fabrica_id}<br>
    Fábrica Nome: {usuario.fabrica.nome if usuario.fabrica else '<strong>SEM FÁBRICA</strong>'}
    """
