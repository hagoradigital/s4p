from itsdangerous import URLSafeSerializer
from flask import current_app


def gerar_token_cliente(cliente_id):
    s = URLSafeSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'cliente_id': cliente_id})


def validar_token_cliente(token):
    s = URLSafeSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return data.get('cliente_id')
    except Exception:
        return None