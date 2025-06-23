# POPULA AS TABELAS COM DADOS INICIAIS

from app import create_app
from extensions import db
from models import (
    Fabrica, Usuario, Cliente, Produto, ProdutoEstoque,
    TipoVestuario, Tamanho, Cor, Pedido, RoleType
)

app = create_app()

with app.app_context():
    print("🚀 Iniciando a população de dados...")

    # ✅ Verificar se já existem fábricas para não duplicar
    if Fabrica.query.first():
        print("⚠️ Banco já possui dados. Abortando população para evitar duplicação.")
        exit()

    # ✅ Fábricas
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
        nome="HD Roupas Ltda",
        cnpj="98.765.432/0001-11",
        email="contato@roupas.com",
        responsavel="Maria Souza",
        celular="(48) 98888-0002",
        status="Ativo",
        tipo="Roupas",
        observacao="Especializada em camisetas promocionais e uniformes."
    )
    f3 = Fabrica(
        nome="HD Padaria Ltda",
        cnpj="56.789.123/0001-44",
        email="contato@padaria.com",
        responsavel="Carlos Lima",
        celular="(48) 97777-0003",
        status="Ativo",
        tipo="Padaria",
        observacao="Foco em panificação artesanal."
    )
    db.session.add_all([f1, f2, f3])
    db.session.commit()

    print("✅ Fábricas cadastradas.")

    # ✅ Tipos de vestuário
    tipos = [
        TipoVestuario(nome="Camiseta", fabrica_id=f1.id),
        TipoVestuario(nome="Moletom", fabrica_id=f1.id),
        TipoVestuario(nome="Uniforme", fabrica_id=f1.id),
        TipoVestuario(nome="Avental", fabrica_id=f3.id)
    ]
    db.session.add_all(tipos)
    db.session.commit()

    print("✅ Tipos de vestuário cadastrados.")

    # ✅ Tamanhos
    tamanhos = [
        Tamanho(descricao="P"),
        Tamanho(descricao="M"),
        Tamanho(descricao="G"),
        Tamanho(descricao="GG"),
        Tamanho(descricao="G1"),
        Tamanho(descricao="G2"),
        Tamanho(descricao="G3")
    ]
    db.session.add_all(tamanhos)
    db.session.commit()

    print("✅ Tamanhos cadastrados.")

    # ✅ Cores
    cores = [
        Cor(descricao="Branco"),
        Cor(descricao="Preto"),
        Cor(descricao="Vermelho"),
        Cor(descricao="Azul"),
        Cor(descricao="Verde"),
        Cor(descricao="Amarelo"),
        Cor(descricao="Cinza")
    ]
    db.session.add_all(cores)
    db.session.commit()

    print("✅ Cores cadastradas.")

    # ✅ Usuários
    usuarios = [
        Usuario(nome="TecMA", email="antunes20@gmail.com", funcao=RoleType.MASTER, fabrica_id=f1.id),
        Usuario(nome="TecAD", email="admin@tec.com", funcao=RoleType.ADMIN, fabrica_id=f1.id),
        Usuario(nome="TecME", email="medio@tec.com", funcao=RoleType.MEDIO, fabrica_id=f1.id),
        Usuario(nome="TecSI", email="simples@tec.com", funcao=RoleType.SIMPLES, fabrica_id=f1.id),

        Usuario(nome="RoupasAD", email="admin@roupas.com", funcao=RoleType.ADMIN, fabrica_id=f2.id),
        Usuario(nome="RoupasME", email="medio@roupas.com", funcao=RoleType.MEDIO, fabrica_id=f2.id),

        Usuario(nome="PadariaAD", email="admin@padaria.com", funcao=RoleType.ADMIN, fabrica_id=f3.id),
    ]

    for u in usuarios:
        u.set_senha("123456")

    db.session.add_all(usuarios)
    db.session.commit()

    print("✅ Usuários cadastrados.")

    # ✅ Produtos com saldo inicial
    produtos = [
        Produto(nome="Camiseta Branca", tipo_id=tipos[0].id, fabrica_id=f1.id, saldo_estoque=100),
        Produto(nome="Moletom Azul", tipo_id=tipos[1].id, fabrica_id=f1.id, saldo_estoque=50),
        Produto(nome="Uniforme Técnico", tipo_id=tipos[2].id, fabrica_id=f1.id, saldo_estoque=30),
        Produto(nome="Avental Branco", tipo_id=tipos[3].id, fabrica_id=f3.id, saldo_estoque=20)
    ]

    db.session.add_all(produtos)
    db.session.commit()

    print("✅ Produtos cadastrados com saldo inicial.")

    # ✅ Registrar entrada inicial no estoque
    tamanho_m = next(t for t in tamanhos if t.descricao == "M")
    cor_branco = next(c for c in cores if c.descricao == "Branco")
    cor_azul = next(c for c in cores if c.descricao == "Azul")

    movimentos = []
    for p in produtos:
        movimento = ProdutoEstoque(
            produto_id=p.id,
            tamanho_id=tamanho_m.id,
            cor_id=cor_branco.id if "Branca" in p.nome or "Avental" in p.nome else cor_azul.id,
            quantidade=p.saldo_estoque,
            tipo_movimento="entrada",
            status_estoque="Estoque",
            usuario_id=usuarios[0].id
        )
        movimentos.append(movimento)

    db.session.add_all(movimentos)
    db.session.commit()

    print("✅ Movimentos de estoque registrados.")

    print("🎯 População concluída com sucesso.")