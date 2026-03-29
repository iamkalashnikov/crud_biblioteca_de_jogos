from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configurando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# modelo ORM completo
class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    plataforma = db.Column(db.String(50))
    genero = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer)
    nota = db.Column(db.Float)

# criação automática das tabelas
with app.app_context():
    db.create_all()


# GET (LISTAR / BUSCAR)

@app.route('/jogos', methods=['GET'])
@app.route('/jogos/<int:id>', methods=['GET'])
def gerenciar_jogos(id=None):

    # busca por ID usando ORM
    if id:
        jogo = Jogo.query.get(id)

        if jogo:
            return jsonify({
                "id": jogo.id,
                "nome": jogo.nome,
                "plataforma": jogo.plataforma,
                "genero": jogo.genero,
                "preco": jogo.preco,
                "estoque": jogo.estoque,
                "nota": jogo.nota
            }), 200

        return jsonify({"erro": "Jogo não encontrado"}), 404

    # listagem usando ORM
    jogos = Jogo.query.all()

    lista_jogos = [{
        "id": j.id,
        "nome": j.nome,
        "plataforma": j.plataforma,
        "genero": j.genero,
        "preco": j.preco,
        "estoque": j.estoque,
        "nota": j.nota
    } for j in jogos]

    return jsonify(lista_jogos), 200


# POST (CRIAR)

@app.route('/insert', methods=['POST'])
def criar_jogo():
    dados = request.get_json()

    # inserção usando ORM
    novo_jogo = Jogo(
        nome=dados.get('nome'),
        plataforma=dados.get('plataforma'),
        genero=dados.get('genero'),
        preco=dados.get('preco'),
        estoque=dados.get('estoque')
    )

    db.session.add(novo_jogo)
    db.session.commit()

    return jsonify({"mensagem": "Jogo criado com sucesso!"}), 201


# PUT (ATUALIZAR)

@app.route('/update/<int:id>', methods=['PUT'])
def atualizar_jogo(id):
    dados = request.get_json()

    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    # atualização usando ORM
    jogo.nome = dados.get('nome')
    jogo.plataforma = dados.get('plataforma')
    jogo.genero = dados.get('genero')
    jogo.preco = dados.get('preco')
    jogo.estoque = dados.get('estoque')

    db.session.commit()

    return jsonify({"mensagem": "Jogo atualizado com sucesso!"}), 200

# DELETE
@app.route('/delete/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    jogo = Jogo.query.get(id)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    db.session.delete(jogo)
    db.session.commit()

    return jsonify({"mensagem": f"Jogo '{jogo.nome}' removido!"}), 200

# AVALIAR

@app.route('/avaliar/<int:id>', methods=['PUT'])
def avaliar_jogo(id):
    dados = request.get_json()
    nota = dados.get('nota')

    if nota is None or nota < 0 or nota > 10:
        return jsonify({"erro": "Nota deve ser entre 0 e 10"}), 400

    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    # atualização usando ORM
    jogo.nota = nota
    db.session.commit()

    return jsonify({"mensagem": "Jogo avaliado com sucesso!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
