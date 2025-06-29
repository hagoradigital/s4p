import os
from flask import Flask
from config import Config
from extensions import db, login_manager, babel, csrf


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # 🔧 Configurações do app
    app.config.from_object(Config)

    # 🔗 Inicializa as extensões
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)

    # 🔥 Filtro personalizado para formatar valores como moeda BR
    def moeda(valor):
        try:
            if valor is None:
                return "R$ 0,00"
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "R$ 0,00"

    app.jinja_env.filters['moeda'] = moeda

    # 🔑 Importa os modelos após db.init_app() para evitar importações circulares
    from models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # 🔹 Registra os blueprints
    from routes.auth import auth_bp
    from routes.usuario import usuario_bp
    from routes.fabrica import fabrica_bp
    from routes.cliente import cliente_bp
    from routes.produto import produto_bp
    from routes.modal_tipo_vestuario import modal_tipo_vestuario_bp
    from routes.estoque import estoque_bp
    from routes.pedido import pedido_bp
    from routes.gerar_link_cliente import gerar_link_bp
    from routes.pdf import pdf_bp
    # from routes.novo_cliente import novo_cliente_bp  # Caso você tenha essa rota ativa

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(fabrica_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(modal_tipo_vestuario_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(gerar_link_bp)
    app.register_blueprint(pdf_bp)
    # app.register_blueprint(novo_cliente_bp)


    # 🔧 Context processor para disponibilizar formulários ou variáveis globais nos templates
    @app.context_processor
    def inject_forms():
        from forms.tipo_vestuario_form import TipoVestuarioForm
        return {"form_tipo": TipoVestuarioForm()}

    return app


# 🔥 Instancia o app para uso no Gunicorn (deploy) e também local
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)