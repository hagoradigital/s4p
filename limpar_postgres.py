import psycopg2

# 🔗 Sua URL de conexão
POSTGRES_URL = "postgresql://sgp_fnsk_user:v3P4TDeMuGBNrzOk0YQWn6QcrFTVQZju@dpg-d1cu3915pdvs73c5vlk0-a.oregon-postgres.render.com/sgp_fnsk"

try:
    print("🚀 Conectando ao PostgreSQL...")
    conn = psycopg2.connect(POSTGRES_URL)
    cursor = conn.cursor()

    tabelas = [
        "permissao",
        "estoque",
        "pedido_item",
        "pedido",
        "produto",
        "cliente",
        "usuario",
        "tipo_vestuario",
        "cor",
        "tamanho",
        "fabrica"
    ]

    for tabela in tabelas:
        print(f"➡️ Limpando tabela: {tabela}")
        cursor.execute(f"DELETE FROM {tabela} CASCADE;")

    conn.commit()
    print("✅ Todas as tabelas foram limpas com sucesso!")

except Exception as e:
    print("❌ Erro ao limpar o banco:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("🔒 Conexão encerrada.")