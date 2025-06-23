# CRIA UM BACKUP DO BANCO DE DADOS ATUAL

import os
import shutil
from datetime import datetime

# 🔧 Configuração do nome do arquivo do banco
DATABASE_FILE = 'sgp.db'  # nome do seu arquivo SQLite

# 🔧 Diretório onde o backup será salvo
BACKUP_DIR = 'backups'

# 🔧 Criar a pasta de backup se não existir
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# 🔧 Gerar o nome do arquivo de backup com data e hora
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = os.path.join(BACKUP_DIR, f'backup_{timestamp}.db')

# 🔧 Verificar se o banco existe
if os.path.exists(DATABASE_FILE):
    shutil.copy2(DATABASE_FILE, backup_file)
    print(f"✅ Backup criado com sucesso: {backup_file}")
else:
    print(f"❌ Banco de dados '{DATABASE_FILE}' não encontrado. Verifique o nome do arquivo.")