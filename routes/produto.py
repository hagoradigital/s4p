from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Produto
from forms.produto_form import ProdutoForm
from models.estoque import Estoque
from sqlalchemy import asc, desc, func

produto_bp = Blueprint("produto", __name__, url_prefix="/produto")


# 🔸 LISTAR E CADASTRAR PRODUTO
@produto_bp.route("/", methods=["GET", "POST"])
@login_required
def produto_listar():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    mostrar_modal = False
    form = ProdutoForm()
    form.carregar_tipos_vestuario()
    form.carregar_tamanhos()
    form.carregar_cores()

    query = Produto.query.filter_by(fabrica_id=current_user.fabrica_id)

    if search and len(search) >= 3:
        like_pattern = f"%{search}%"
        query = query.filter(Produto.nome.ilike(like_pattern))

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                valor_compra = float(form.valor_compra.data.replace(".", "").replace(",", "."))
                valor_venda = float(form.valor_venda.data.replace(".", "").replace(",", "."))

                # 🔥 Tratamento do status
                # status = "ativo" if form.status.data == 1 else "inativo"
                status = form.status.data if form.status.data in ['ativo', 'inativo'] else 'ativo'

                novo_produto = Produto(
                    nome=form.nome.data,
                    tipo_id=form.tipo_id.data,
                    tamanho_id=form.tamanho_id.data,
                    cor_id=form.cor_id.data,
                    descricao=form.descricao.data,
                    status=form.status.data,
                    valor_compra=valor_compra,
                    valor_venda=valor_venda,
                    fabrica_id=current_user.fabrica_id
                )

                db.session.add(novo_produto)
                db.session.commit()

                flash("Produto cadastrado com sucesso!", "success")
                return redirect(url_for("produto.produto_listar"))

            except Exception as e:
                db.session.rollback()
                print(f"❌ Erro ao salvar produto: {e}")
                flash("Erro ao cadastrar produto. Verifique os campos.", "danger")
                mostrar_modal = True

        else:
            flash("Erro ao cadastrar produto. Verifique os campos obrigatórios.", "danger")
            mostrar_modal = True

    coluna = getattr(Produto, order_by, Produto.nome)
    coluna = func.lower(coluna)
    coluna = coluna.desc() if order_dir == "desc" else coluna.asc()

    produtos = query.order_by(coluna).paginate(page=page, per_page=15)

    conteudo = render_template("admin/produto_listar.html",
                               produtos=produtos,
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


# 🔸 EDITAR PRODUTO
@produto_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)

    form = ProdutoForm()
    form.carregar_tipos_vestuario()
    form.carregar_tamanhos()
    form.carregar_cores()

    if form.validate_on_submit():
        try:
            produto.nome = form.nome.data
            produto.tipo_id = form.tipo_id.data
            produto.tamanho_id = form.tamanho_id.data
            produto.cor_id = form.cor_id.data
            produto.descricao = form.descricao.data
            produto.valor_compra = float(form.valor_compra.data.replace(".", "").replace(",", "."))
            produto.valor_venda = float(form.valor_venda.data.replace(".", "").replace(",", "."))

            # 🔥 Tratamento do status
            # produto.status = "ativo" if form.status.data == 1 else "inativo"
            # produto.status = form.status.data if form.status.data in ['ativo', 'inativo'] else 'ativo'
            produto.status = form.status.data

            db.session.commit()
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("produto.produto_listar"))

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao editar produto: {e}")
            flash("Erro ao atualizar produto. Verifique os campos.", "danger")
            mostrar_modal = "editar"

    else:
        flash("Erro ao atualizar produto. Verifique os campos obrigatórios.", "danger")
        mostrar_modal = "editar"

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    order_by = request.args.get("order_by", "nome")
    order_dir = request.args.get("order_dir", "asc")

    sort_column = getattr(Produto, order_by, Produto.nome)
    sort_order = asc(func.lower(sort_column)) if order_dir == "asc" else desc(func.lower(sort_column))

    produtos = Produto.query.filter_by(fabrica_id=current_user.fabrica_id).order_by(sort_order).paginate(page=page, per_page=15)

    conteudo = render_template("admin/produto_listar.html",
                               produtos=produtos,
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


# 🔸 EXCLUIR PRODUTO
@produto_bp.route("/excluir/<int:id>", methods=["POST"])
@login_required
def produto_excluir(id):
    produto = Produto.query.get_or_404(id)

    # Verificar se existem movimentações de estoque vinculadas
    movimentacoes = Estoque.query.filter_by(produto_id=produto.id).all()

    if movimentacoes:
        flash('Não é possível excluir este produto, pois existem movimentações de estoque vinculadas.', 'danger')
        return redirect(url_for('produto.produto_listar'))

    try:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir produto: {str(e)}', 'danger')

    return redirect(url_for('produto.produto_listar'))