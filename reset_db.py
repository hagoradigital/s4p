# CRIA TODAS AS TABELAS SEM DADOS INICIAIS

from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    confirm = input("⚠️ Isso irá APAGAR COMPLETAMENTE o banco de dados. Deseja continuar? (s/n): ")
    if confirm.lower() == 's':
        print("🚨 Apagando todas as tabelas...")
        db.drop_all()
        print("✔️ Tabelas removidas com sucesso.")

        print("🛠️ Criando novas tabelas...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso.")

        print("🎯 Banco de dados resetado e pronto para uso.")
    else:
        print("❌ Operação cancelada.")