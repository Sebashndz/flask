from wtforms import Form
from wtforms import StringField, TextField
#from wtforms.fields, html5 import EmailField
from wtforms import validators 

class ConsultaNit(Form):
	nit = TextField('Digite el Nit a consultar:',
					[validators.Required(message='Debe ingresar un Nit.'),
					 validators.length(min=9, max=10, message='Digite un Nit válido.')])
		
		