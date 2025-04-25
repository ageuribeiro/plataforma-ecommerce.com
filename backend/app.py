"""Importing libraries"""
import os
from flask import Flask, jsonify # type: ignore


app = Flask(__name__)


@app.route("/")
def home():
    """Rota Inicial"""
    return jsonify({"message":"Bem-vindo à API do E-commerce!"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
