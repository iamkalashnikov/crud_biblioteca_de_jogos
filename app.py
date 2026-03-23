from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def executar_query(query, *args, fetch=False, commit=False):
    conn = sqlite3.connect('biblioteca_jogos.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    resultado = None
    
    try:
        cursor.execute(query, args)
        
        if commit:
            conn.commit()
        if fetch:
            resultado = cursor.fetchall()
    finally:
        conn.close()
    
    return resultado

@app.route('/jogos', methods=['GET'])
@app.route('/jogos/<int:id>', methods=['GET'])
def gerenciar_jogos(id=None):
    if id:
        jogo = executar_query("SELECT * FROM jogos WHERE id = ?", id, fetch=True)
        if jogo:
            return jsonify(dict(jogo[0])), 200
        return jsonify({"erro": "Jogo não encontrado"}), 404

    dados = executar_query("SELECT * FROM jogos", fetch=True)
    lista_jogos = [dict(item) for item in dados]
    return jsonify(lista_jogos), 200

@app.route('/insert', methods=['POST'])
def criar_jogo():
    dados = request.get_json()
    
    executar_query(
        """INSERT INTO jogos (nome, plataforma, genero, preco, estoque) 
           VALUES (?, ?, ?, ?, ?)""",
        dados.get('nome'),
        dados.get('plataforma'),
        dados.get('genero'),
        dados.get('preco'),
        dados.get('estoque'),
        commit=True
    )
    
    return jsonify({"mensagem": "Jogo criado com sucesso!"}), 201

@app.route('/update/<int:id>', methods=['PUT'])
def atualizar_jogo(id):
    dados = request.get_json()
    
    existe = executar_query("SELECT id FROM jogos WHERE id = ?", id, fetch=True)
    if not existe:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    executar_query(
        """UPDATE jogos 
           SET nome = ?, plataforma = ?, genero = ?, preco = ?, estoque = ?
           WHERE id = ?""",
        dados.get('nome'),
        dados.get('plataforma'),
        dados.get('genero'),
        dados.get('preco'),
        dados.get('estoque'),
        id,
        commit=True
    )
    
    return jsonify({"mensagem": "Jogo atualizado com sucesso!"}), 200

@app.route('/delete/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    jogo = executar_query("SELECT nome FROM jogos WHERE id = ?", id, fetch=True)
    
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    executar_query("DELETE FROM jogos WHERE id = ?", id, commit=True)
    
    return jsonify({"mensagem": f"Jogo '{jogo[0]['nome']}' removido!"}), 200

@app.route('/avaliar/<int:id>', methods=['PUT'])
def avaliar_jogo(id):
    dados = request.get_json()
    
    nota = dados.get('nota')

    if nota is None or nota < 0 or nota > 10:
        return jsonify({"erro": "Nota deve ser entre 0 e 10"}), 400

    existe = executar_query("SELECT id FROM jogos WHERE id = ?", id, fetch=True)
    if not existe:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    executar_query(
        "UPDATE jogos SET nota = ? WHERE id = ?",
        nota, id,
        commit=True
    )

    return jsonify({"mensagem": "Jogo avaliado com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)