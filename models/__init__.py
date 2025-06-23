from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # usa a instância global

from .fabrica import Fabrica
from .usuario import Usuario, RoleType
from .cliente import Cliente
from .tipo_vestuario import TipoVestuario
from .produto import Produto
from .estoque import Estoque
from .tamanho import Tamanho
from .cor import Cor
from .pedido import Pedido, PedidoItem

__all__ = [
    "Fabrica",
    "Usuario",
    "RoleType",
    "Cliente",
    "TipoVestuario",
    "Produto",
    "Estoque",
    "Tamanho",
    "Cor",
    "Pedido",
    "PedidoItem"
]