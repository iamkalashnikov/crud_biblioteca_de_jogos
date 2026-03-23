import sqlite3

conn = sqlite3.connect('biblioteca_jogos.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM jogos")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='jogos'")

conn.commit()
conn.close()

print("Banco resetado com IDs voltando para o 1!")