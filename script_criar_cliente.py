from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

# Conecte-se ao banco SQLite
engine = create_engine("sqlite:///sgp.db")
metadata = MetaData()

# Reflete as tabelas existentes
metadata.reflect(bind=engine)

# Garante que a tabela fabrica está carregada no metadata
if "fabrica" not in metadata.tables:
    raise Exception("Tabela 'fabrica' não foi encontrada. Verifique se ela existe no banco de dados.")

# Define nova tabela Cliente
cliente_table = Table(
    "cliente", metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(120), nullable=False),
    Column("endereco", String(150), nullable=False),
    Column("numero", String(20), nullable=False),
    Column("complemento", String(100)),
    Column("cidade", String(100), nullable=False),
    Column("uf", String(2), nullable=False),
    Column("cep", String(10), nullable=False),
    Column("cnpj", String(18), nullable=False),
    Column("responsavel", String(100), nullable=False),
    Column("cpf_responsavel", String(14), nullable=False),
    Column("celular", String(20), nullable=False),
    Column("telefone", String(20)),
    Column("email", String(120), nullable=False),
    Column("fabrica_id", Integer, ForeignKey("fabrica.id"), nullable=False),
    extend_existing=True
)

# Cria a tabela cliente
with engine.connect() as connection:
    cliente_table.create(connection, checkfirst=True)

print("✅ Tabela 'cliente' criada com sucesso.")