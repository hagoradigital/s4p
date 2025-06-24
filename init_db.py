# CRIA TODAS AS TABELAS E POPULA COM DADOS INICIAIS

from app import create_app
from extensions import db
from models.fabrica import Fabrica
from models.usuario import Usuario, RoleType
from models.cliente import Cliente
from models.tipo_vestuario import TipoVestuario
from models.produto import Produto
from models.estoque import Estoque
from models.tamanho import Tamanho
from models.cor import Cor

app = create_app()

with app.app_context():
    confirm = input("⚠️ Isso irá apagar o banco atual. Deseja continuar? (s/n): ")
    if confirm.lower() == 's':
        db.drop_all()
        db.create_all()
        print("✔️ Banco resetado.")
    else:
        print("❌ Operação cancelada.")
        exit()

    print("✔️ Tabelas criadas:", db.inspect(db.engine).get_table_names())

    # ✅ Fábricas
    f1 = Fabrica(
        nome="HD Tecnologia Ltda",
        cnpj="12.345.678/0001-99",
        email="contato@hd.com.br",
        responsavel="Clayton Antunes",
        celular="(48) 99958-0587",
        status="Ativo",
        tipo="Tecnologia",
        observacao="Foco em software e automação."
    )
    f2 = Fabrica(
        nome="HD Roupas Ltda",
        cnpj="98.765.432/0001-11",
        email="contato@roupas.com.br",
        responsavel="Magda Renata",
        celular="(48) 98484-0587",
        status="Ativo",
        tipo="Roupas",
        observacao="Especializada em camisetas promocionais e uniformes."
    )
    db.session.add_all([f1, f2])
    db.session.commit()

    print("✅ Fábricas cadastradas.")

    # ✅ Tipos de vestuário
    tipos = [
        TipoVestuario(nome="Camiseta", fabrica_id=f2.id),
        TipoVestuario(nome="Moletom", fabrica_id=f2.id),
        TipoVestuario(nome="Uniforme", fabrica_id=f2.id),
        TipoVestuario(nome="Avental", fabrica_id=f2.id)
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

    ]

    for u in usuarios:
        u.set_senha("123")

    db.session.add_all(usuarios)
    db.session.commit()

    print("✅ Usuários cadastrados.")

    # ✅ Produtos com saldo inicial
    tamanho_m = next(t for t in tamanhos if t.descricao == "M")
    tamanho_g = next(t for t in tamanhos if t.descricao == "G")
    cor_branco = next(c for c in cores if c.descricao == "Branco")
    cor_azul = next(c for c in cores if c.descricao == "Azul")

    produtos = [
        Produto(nome="Camiseta Branca M", tipo_id=tipos[0].id, tamanho_id=tamanho_m.id, cor_id=cor_branco.id,
                fabrica_id=f2.id, saldo_estoque=100, valor_compra=10.0, valor_venda=30.0, status="ativo"),

        Produto(nome="Moletom Azul G", tipo_id=tipos[1].id, tamanho_id=tamanho_g.id, cor_id=cor_azul.id,
                fabrica_id=f2.id, saldo_estoque=50, valor_compra=20.0, valor_venda=60.0, status="ativo"),

        Produto(nome="Uniforme Técnico G", tipo_id=tipos[2].id, tamanho_id=tamanho_g.id, cor_id=cor_azul.id,
                fabrica_id=f2.id, saldo_estoque=30, valor_compra=15.0, valor_venda=45.0, status="ativo"),

        Produto(nome="Avental Branco M", tipo_id=tipos[3].id, tamanho_id=tamanho_m.id, cor_id=cor_branco.id,
                fabrica_id=f3.id, saldo_estoque=20, valor_compra=12.0, valor_venda=35.0, status="ativo")
    ]

    db.session.add_all(produtos)
    db.session.commit()

    print("✅ Produtos cadastrados com saldo inicial.")

    # ✅ Registrar entrada inicial no estoque
    movimentos = []
    for p in produtos:
        movimento = Estoque(
            produto_id=p.id,
            quantidade=p.saldo_estoque,
            tipo_movimento="entrada",
            status_estoque="Estoque",
            usuario_id=usuarios[0].id,
            fabrica_id=p.fabrica_id,
            local_compra="Estoque inicial"
        )
        movimentos.append(movimento)

    db.session.add_all(movimentos)
    db.session.commit()

    print("✅ Movimentos de estoque registrados.")

    print("🎯 Banco criado com sucesso e pronto para uso.")