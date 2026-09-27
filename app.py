from flask import Flask, render_template, redirect, request, flash, url_for

from flask_login import login_required, login_user, logout_user, LoginManager

from werkzeug.security import generate_password_hash, check_password_hash

from models.forms import RegisterForm, LoginForm

from models.db import db

from flask_migrate import Migrate

from models.tables import User, Caixa

import os

from flask import request



migrate = Migrate()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)
migrate.init_app(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#===========================================================================



@app.template_filter("moeda")
def moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")




@app.route("/", methods=["GET"])
@login_required
def home():
    movimentacoes = Caixa.query.all()
    
    total_entradas = 0
    total_saidas = 0
    
    for movimentacao in movimentacoes:
        if movimentacao.tipo == "entrada":
            total_entradas += movimentacao.valor
            
        elif movimentacao.tipo == "saida":
            total_saidas += movimentacao.valor
            
            
    saldo = total_entradas - total_saidas
    
    
    return render_template('index.html', 
                           movimentacoes=movimentacoes,
                           total_entradas=total_entradas,
                           total_saidas=total_saidas,
                           saldo=saldo)

#==============================================================================================
#==============================================================================================
#==============================================================================================



#AUTENTICATE

@app.route("/registro", methods=["POST", "GET"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        senha = form.senha.data
        senha_hash = generate_password_hash(senha)

        usuario = User(
            nome=form.nome.data,
            email=form.email.data,
            senha=senha_hash
        )

        db.session.add(usuario)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html", form=form)
    
    
    
    
    
    

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and user.check_senha(form.senha.data):

            login_user(user)

            flash("Login realizado com sucesso")
            print("login realizado")

            return redirect(url_for("home"))

        else:
            print("Usuário ou senha incorretos")

    else:
        print(form.errors)

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")


#==============================================================================================
#==============================================================================================
#==============================================================================================



@app.route("/caixa", methods=["POST"])
@login_required
def caixa():
    tipo = request.form["tipo"]
    modalidade = request.form["modalidade"]
    categoria = request.form["categoria"]
    valor = request.form["valor"]
    descricao = request.form["descricao"]
    
    movimentacao = Caixa(
        tipo=tipo,
        modalidade=modalidade,
        categoria=categoria,
        valor=valor,
        descricao=descricao
    )
    
    db.session.add(movimentacao)
    db.session.commit()
    
    return redirect(url_for("home"))



@app.route("/movimentacoes", methods=['POST', 'GET'])
@login_required
def movimentacoes():
    movimentacoes = Caixa.query.all()
    
    return render_template("movimentacoes.html", movimentacoes=movimentacoes)





@app.route("/caixa/modalidade", methods=["GET", "POST"])  
@login_required
def modalidade():
    
    movimentacoes = Caixa.query.all()
    
    
    entrada_masculino = 0
    saida_masculino = 0

    entrada_feminino = 0
    saida_feminino = 0

    entrada_misto = 0
    saida_misto = 0

    for movimentacao in movimentacoes:

        if movimentacao.modalidade == "masculino":

            if movimentacao.tipo == "entrada":
                entrada_masculino += movimentacao.valor

            elif movimentacao.tipo == "saida":
                saida_masculino += movimentacao.valor


        elif movimentacao.modalidade == "feminino":

            if movimentacao.tipo == "entrada":
                entrada_feminino += movimentacao.valor

            elif movimentacao.tipo == "saida":
                saida_feminino += movimentacao.valor


        elif movimentacao.modalidade == "misto":

            if movimentacao.tipo == "entrada":
                entrada_misto += movimentacao.valor

            elif movimentacao.tipo == "saida":
                saida_misto += movimentacao.valor
    
    saldo_masculino = entrada_masculino - saida_masculino
    saldo_feminino = entrada_feminino - saida_feminino
    saldo_misto = entrada_misto - saida_misto
    
    return render_template("modalidade.html", 
                           entrada_masculino=entrada_masculino,
                            entrada_feminino=entrada_feminino,
                            entrada_misto=entrada_misto,

                            saida_masculino=saida_masculino,
                            saida_feminino=saida_feminino,
                            saida_misto=saida_misto,

                            saldo_masculino=saldo_masculino,
                            saldo_feminino=saldo_feminino,
                            saldo_misto=saldo_misto
                                        )
      
    
    
    



if __name__ == "__main__":
    app.run(
        debug= True,
        host="0.0.0.0",
        port=5000
    )