from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length

# from wtforms.fields, html5 import EmailField
from wtforms import validators

class ConsultaNit(Form):
    nit = TextField(
        "Digite el Nit a consultar:",
        [
            validators.Required(message="Debe ingresar un Nit."),
            validators.length(min=9, max=10, message="Digite un Nit válido."),
        ],
    )

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
	first_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
	last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	roles = SelectField(u'Role',choices = [('A','a'), ('B','b'), ('C','c')],validators=[DataRequired()])
	submit = SubmitField('Registrar')

class UpdateForm(FlaskForm):
	first_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
	last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	roles = SelectField(u'Role',choices = [('A','a'), ('B','b'), ('C','c')],validators=[DataRequired()])
	submit = SubmitField('Actualizar')