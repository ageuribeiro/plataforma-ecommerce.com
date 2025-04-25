from flask import Flask, redirect, request, render_template, jsonify  # type: ignore


app = Flask(__name__)


@app.route("/")
def home():
    """Rota Inicial"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
