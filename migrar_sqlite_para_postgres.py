import sqlite3
import psycopg2
from psycopg2 import sql

# ✅ Caminho do banco SQLite
SQLITE_DB = 'instance/sgp.db'

# ✅ URL do PostgreSQL (ajuste conforme seu Render)
POSTGRES_URL = 'postgresql://sgp_fnsk_user:v3P4TDeMuGBNrzOk0YQWn6QcrFTVQZju@dpg-d1cu3915pdvs73c5vlk0-a.oregon-postgres.render.com/sgp_fnsk'

# ✅ Ordem de migração considerando dependências (tabelas pai primeiro)
TABELAS = [
    "fabrica",
    "tamanho",
    "cor",
    "tipo_vestuario",
    "usuario",
    "cliente",
    "produto",
    "pedido",
    "pedido_item",
    "estoque",
    "permissao"
]

print("✅ Conectando aos bancos...")

# 🔗 Conectar SQLite
sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_cursor = sqlite_conn.cursor()

# 🔗 Conectar PostgreSQL
postgres_conn = psycopg2.connect(POSTGRES_URL)
postgres_cursor = postgres_conn.cursor()

print("🚀 Conectado ao SQLite e PostgreSQL")

for table in TABELAS:
    print(f"\n➡️ Migrando tabela: {table}")

    try:
        # 🔍 Buscar dados do SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        rows = sqlite_cursor.fetchall()

        if not rows:
            print(f"⚠️ Nenhum registro na tabela {table}")
            continue

        # 🔍 Buscar colunas da tabela
        colunas = [description[0] for description in sqlite_cursor.description]
        colunas_sql = ", ".join(colunas)
        placeholders = ", ".join(["%s"] * len(colunas))

        # 🔨 Query de insert
        insert_query = sql.SQL(
            f"INSERT INTO {table} ({colunas_sql}) VALUES ({placeholders})"
        )

        for row in rows:
            row = list(row)

            # ✔️ Ajuste específico para campo booleano
            if table == "usuario":
                idx_ativo = colunas.index('ativo')
                if row[idx_ativo] == 1:
                    row[idx_ativo] = True
                elif row[idx_ativo] == 0 or row[idx_ativo] is None:
                    row[idx_ativo] = False
                else:
                    row[idx_ativo] = bool(row[idx_ativo])

            postgres_cursor.execute(insert_query, row)

        postgres_conn.commit()
        print(f"✅ {len(rows)} registros migrados na tabela {table}")

    except Exception as e:
        postgres_conn.rollback()
        print(f"❌ Erro ao migrar tabela {table}: {e}")

# 🔒 Encerrar conexões
sqlite_conn.close()
postgres_cursor.close()
postgres_conn.close()

print("\n🎉 Migração concluída com sucesso!")