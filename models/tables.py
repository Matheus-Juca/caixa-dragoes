from models.db import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome =  db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(255))
    
    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    
    
    
class Caixa(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(db.String(20), nullable=False)

    categoria = db.Column(db.String(50), nullable=False)
    
    modalidade = db.Column(db.String(20), nullable=False)

    valor = db.Column(db.Float, nullable=False)

    descricao = db.Column(db.String(255))

    data = db.Column(db.DateTime, default=datetime.now)