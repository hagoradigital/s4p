from app import create_app
from extensions import db
from models import Fabrica, Usuario, Cliente, RoleType

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    f1 = Fabrica(
        nome="HD Tecnologia Ltda",
        cnpj="12.345.678/0001-99",
        email="contato@tec.com",
        responsavel="João Silva",
        celular="(48) 99999-0001",
        status="Ativo",
        tipo="Tecnologia",
        observacao="Foco em software e automação."
    )

    f2 = Fabrica(
        nome="HD Roupas ltda",
        cnpj="98.765.432/0001-11",
        email="contato@roupas.com",
        responsavel="Maria Souza",
        celular="(48) 98888-0002",
        status="Ativo",
        tipo="Roupas",
        observacao="Especializada em camisetas promocionais e uniformes."
    )

    f3 = Fabrica(
        nome="HD Padaria ltda",
        cnpj="98.765.432/0001-11",
        email="contato@roupas.com",
        responsavel="Maria Souza",
        celular="(48) 98888-0002",
        status="Ativo",
        tipo="Roupas",
        observacao="Especializada em camisetas promocionais e uniformes."
    )

    db.session.add_all([f1, f2, f3])
    db.session.commit()

    u1 = Usuario(
        nome="TecMA",
        email="antunes20@gmail.com",
        funcao=RoleType.MASTER,
        fabrica_id=f1.id
    )
    u1.set_senha("123456")

    u2 = Usuario(
        nome="TecAD",
        email="admin@tec.com",
        funcao=RoleType.ADMIN,
        fabrica_id=f1.id
    )
    u2.set_senha("123456")

    u3 = Usuario(
        nome="TecME",
        email="medio@tec.com",
        funcao=RoleType.MEDIO,
        fabrica_id=f1.id
    )
    u3.set_senha("123456")

    u4 = Usuario(
        nome="TecSI",
        email="simples@tec.com",
        funcao=RoleType.SIMPLES,
        fabrica_id=f1.id
    )
    u4.set_senha("123456")

    u5 = Usuario(
        nome="RoupasAD",
        email="admin@roupas.com",
        funcao=RoleType.ADMIN,
        fabrica_id=f2.id
    )
    u5.set_senha("123456")

    u6 = Usuario(
        nome="RoupasME",
        email="medio@roupas.com",
        funcao=RoleType.MEDIO,
        fabrica_id=f2.id
    )
    u6.set_senha("123456")

    u7 = Usuario(
        nome="PadariaAD",
        email="admin@padaria.com",
        funcao=RoleType.ADMIN,
        fabrica_id=f3.id
    )
    u7.set_senha("123456")

    db.session.add_all([u1, u2, u3, u4, u5, u6, u7])
    db.session.commit()

    print("✅ Banco criado com sucesso com fábricas completas e usuários.")
