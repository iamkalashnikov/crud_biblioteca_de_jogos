# CRUD de Biblioteca de Jogos

Este é um projeto simples de API REST desenvolvido com **Flask** e **SQLite**, que permite gerenciar uma biblioteca de jogos.

## Funcionalidades

-  Listar todos os jogos
-  Buscar um jogo por ID
-  Adicionar um novo jogo
-  Atualizar um jogo existente
-  Deletar um jogo
-  Avaliar um jogo (nota de 0 a 10)

---

## Tecnologias utilizadas

- Python
- Flask
- SQLite3

---

##  Estrutura do projeto

/projeto
│── app.py
│── biblioteca_jogos.db
│── criar_tabela.py
│── resetar_banco.py
│── alterar_tabela.py


---

## Como executar o projeto

### 1. Instalar dependências
### 2. Executar o servidor

### As rotas da API para teste são:

GET /jogos
GET /jogos/<id>
POST /insert
PUT /update/<id>
DELETE /delete/<id>
**E O DIFERENCIAL COM UMA FUNCIONALIDADE INCREMENTADA NO CODIGO DE REFERÊNCIA QUE É AVALIAR O JOGO**
PUT /avaliar/<id>

### O teste foi realizado no postman e é recomendado que seja feito no mesmo.
