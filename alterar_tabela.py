import sqlite3

conn = sqlite3.connect('biblioteca_jogos.db')
cursor = conn.cursor()

cursor.execute("ALTER TABLE jogos ADD COLUMN nota REAL DEFAULT 0;")

conn.commit()
conn.close()

print("Coluna 'nota' adicionada com sucesso!")