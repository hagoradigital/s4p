from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import TipoVestuario
from forms.tipo_vestuario_form import TipoVestuarioForm

modal_tipo_vestuario_bp = Blueprint("modal_tipo_vestuario", __name__)

# ✅ NOVA ROTA: Carrega o HTML da modal via Ajax
@modal_tipo_vestuario_bp.route("/modal/tipo-vestuario/html", methods=["GET"])
@login_required
def modal_tipo_vestuario_html():
    form = TipoVestuarioForm()
    tipos = TipoVestuario.query.filter_by(fabrica_id=current_user.fabrica_id).all()
    return render_template("admin/modais/tipo_vestuario.html", form_tipo=form, tipos_vestuario=tipos)

# ✅ Rota que salva o novo tipo de vestuário
@modal_tipo_vestuario_bp.route("/modal/tipo-vestuario", methods=["POST"])
@login_required
def salvar_tipo_vestuario():
    form = TipoVestuarioForm()
    if form.validate_on_submit():
        novo_tipo = TipoVestuario(
            nome=form.nome.data,
            fabrica_id=current_user.fabrica_id
        )
        db.session.add(novo_tipo)
        db.session.commit()
        flash("Tipo de vestuário cadastrado com sucesso!", "success")
    else:
        flash("Erro ao salvar o tipo de vestuário. Verifique os dados.", "danger")
    return redirect(url_for("auth.dashboard"))

# ✅ Rota que exclui o tipo de vestuário
@modal_tipo_vestuario_bp.route("/modal/tipo-vestuario/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_tipo_vestuario(id):
    tipo = TipoVestuario.query.get_or_404(id)
    if tipo.produtos:
        flash("Este tipo de vestuário está vinculado a produtos e não pode ser excluído.", "warning")
        return redirect(url_for("auth.dashboard"))
    db.session.delete(tipo)
    db.session.commit()
    flash("Tipo de vestuário excluído com sucesso!", "success")
    return redirect(url_for("auth.dashboard"))