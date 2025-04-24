from flask import Flask, redirect, render_template, request
from models.user import User
from database import usuarios


def listar_usuarios():
    return render_template("user_view.html", usuarios= usuarios)

def adicionar_usuarios():
    nome = request.form['nome']
    email = request.form['email']
    novo_usuario = User(nome, email)
    usuarios.append(novo_usuario)
    return redirect('/usuarios')
