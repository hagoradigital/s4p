import psycopg2

# 🔗 Conexão com PostgreSQL
conn = psycopg2.connect(
    dbname="sgp_fnsk",
    user="sgp_fnsk_user",
    password="v3P4TDeMuGBNrzOk0YQWn6QcrFTVQZju",
    host="dpg-d1cu3915pdvs73c5vlk0-a.oregon-postgres.render.com",
    port="5432"
)

cursor = conn.cursor()

try:
    # Cria as tabelas no PostgreSQL
    print("🚀 Criando tabelas no PostgreSQL...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fabrica (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cnpj VARCHAR(20),
            email VARCHAR(120),
            responsavel VARCHAR(100),
            celular VARCHAR(20),
            status VARCHAR(10),
            tipo VARCHAR(50),
            observacao TEXT,
            created_at TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tamanho (
            id SERIAL PRIMARY KEY,
            descricao VARCHAR(10) UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cor (
            id SERIAL PRIMARY KEY,
            descricao VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipo_vestuario (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            fabrica_id INTEGER REFERENCES fabrica(id) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            senha_hash VARCHAR(128) NOT NULL,
            funcao VARCHAR(20) NOT NULL,
            ativo BOOLEAN,
            created_at TIMESTAMP,
            fabrica_id INTEGER REFERENCES fabrica(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            endereco VARCHAR(150),
            numero VARCHAR(20),
            complemento VARCHAR(100),
            cidade VARCHAR(100),
            uf VARCHAR(2),
            cep VARCHAR(10),
            cnpj VARCHAR(18),
            cpf VARCHAR(14),
            responsavel VARCHAR(100),
            celular VARCHAR(20),
            telefone VARCHAR(20),
            email VARCHAR(120),
            fabrica_id INTEGER REFERENCES fabrica(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produto (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            descricao TEXT,
            tipo_id INTEGER REFERENCES tipo_vestuario(id) NOT NULL,
            fabrica_id INTEGER REFERENCES fabrica(id) NOT NULL,
            tamanho_id INTEGER REFERENCES tamanho(id) NOT NULL,
            cor_id INTEGER REFERENCES cor(id) NOT NULL,
            status VARCHAR(20) NOT NULL,
            valor_compra NUMERIC(10,2) NOT NULL,
            valor_venda NUMERIC(10,2) NOT NULL,
            saldo_estoque INTEGER NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido (
            id SERIAL PRIMARY KEY,
            fabrica_id INTEGER REFERENCES fabrica(id) NOT NULL,
            numero INTEGER NOT NULL,
            cliente_id INTEGER REFERENCES cliente(id) NOT NULL,
            data TIMESTAMP,
            valor_frete NUMERIC(10,2) NOT NULL,
            status VARCHAR(20) NOT NULL,
            usuario_id INTEGER REFERENCES usuario(id) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido_item (
            id SERIAL PRIMARY KEY,
            pedido_id INTEGER REFERENCES pedido(id) NOT NULL,
            produto_id INTEGER REFERENCES produto(id) NOT NULL,
            quantidade INTEGER NOT NULL,
            informacao VARCHAR(100)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id SERIAL PRIMARY KEY,
            fabrica_id INTEGER REFERENCES fabrica(id) NOT NULL,
            produto_id INTEGER REFERENCES produto(id) NOT NULL,
            quantidade INTEGER NOT NULL,
            tipo_movimento VARCHAR(10) NOT NULL,
            status_estoque VARCHAR(20),
            usuario_id INTEGER REFERENCES usuario(id) NOT NULL,
            data_movimento TIMESTAMP,
            referencia_entrada_id INTEGER,
            valor_unitario NUMERIC(10,2),
            local_compra TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permissao (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES usuario(id),
            acao VARCHAR(50) NOT NULL,
            permitido BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)

    conn.commit()
    print("✅ Todas as tabelas foram criadas com sucesso no PostgreSQL!")

except Exception as e:
    conn.rollback()
    print(f"❌ Erro ao criar tabelas: {e}")

finally:
    cursor.close()
    conn.close()
    print("🔒 Conexão encerrada.")