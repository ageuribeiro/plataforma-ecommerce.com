"""Importing libraries"""
import os
from flask import Flask, jsonify # type: ignore


app = Flask(__name__)


@app.route("/")
def home():
    """Rota Inicial"""
    return jsonify({"message":"Bem-vindo à API do E-commerce!"})


if __name__ == '__main__':
    app.run(debug=True)
