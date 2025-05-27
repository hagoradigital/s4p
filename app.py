import os
from flask import Flask
from config import Config
from extensions import db, login_manager, babel

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Caminho correto para o banco dentro de /instance
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'sgp.db')
    app.config.from_object(Config)

    # Inicializa as extensões com o app
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    # Importa os modelos somente após o db.init_app()
    from models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Registra os blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    from routes.fabrica import fabrica_bp
    app.register_blueprint(fabrica_bp)

    from routes.cliente import cliente_bp
    app.register_blueprint(cliente_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)