from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm) :
    nome = StringField("nome", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    senha = PasswordField("senha", validators=[DataRequired()])
    submit = SubmitField("Cadastrar")
    
class LoginForm(FlaskForm) :
    email = StringField("email", validators=[DataRequired(), Email()])
    senha = PasswordField("senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")
    