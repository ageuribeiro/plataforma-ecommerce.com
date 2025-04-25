"""Importing libraries"""
import os
import logging
from flask import Flask, jsonify, request  # type: ignore
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# Permite todas as origens (para desenvolvimento)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Para produção, liste apenas o domínio do seu Netlify:
# CORS(app, resources={r"/api/*": {"origins": ["https://seu-frontend-netlify.netlify.app"]}})

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_default_database()
produtos_collection = db['produtos']


@app.route("/")
def home():
    """Rota Inicial"""
    return jsonify({"message": "Bem-vindo à API do E-commerce!"})


@app.route("/api/produtos", methods=['GET'])
def all_produtos():
    """Rota pra listar todos os produtos"""
    try:
        produtos_cursor = produtos_collection.find()
        produtos = []
        for produto in produtos_cursor:
            produto['_id'] = str(produto['_id'])
            produtos.append(produto)

        logging.info(f"Produtos listados com sucesso. Total de produtos: {len(produtos)}")
        return jsonify(produtos)

    except Exception as e:
        logging.error(f"Erro ao listar produtos do MongoDB: {e}")
        return jsonify({"erro": "Erro ao buscar produtos"}), 500

@app.route("/api/produtos", methods=['POST'])
def adicionar_produto():
    """Rota para adicionar um novo produto ao MongoDB"""
    try:
        novo_produto = request.get_json()
        if not novo_produto:
            return jsonify({"erro": "Nenhum dado de produto fornecido"}), 400

        inserted_id = produtos_collection.insert_one(novo_produto).inserted_id
        logging.info(f"Produto adicionado com sucesso. ID: {inserted_id}")
        novo_produto['_id'] = str(inserted_id) # Adicionar o ID como string para a resposta
        return jsonify(novo_produto), 201
    except Exception as e:
        logging.error(f"Erro ao adicionar produto ao MongoDB: {e}")
        return jsonify({"erro": "Erro ao adicionar produto"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
