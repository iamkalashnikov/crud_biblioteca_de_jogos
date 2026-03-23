import sqlite3

conn = sqlite3.connect('biblioteca_jogos.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    plataforma TEXT NOT NULL,
    genero TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL,
    nota REAL DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")