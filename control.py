from flask import Flask, render_template	
from flask import request
import forms


#from zeep import Client
#import os
#import codecs

from Divisa_Functions import webservice_request, connectionDB, save_dataframe

app = Flask(__name__, static_url_path="/Static")

@app.route('/', methods=['GET', 'POST'])
def index():
	#return ("Hola Mundo")
	#Directorio = os.getcwd() + "\\"
	
	#PathCarpetaConsultas = Directorio +"Consultas\\"
	#PathCarpetaConsultas = "C:\\Python_Flask\\envDivisa\\Consultas\\"
	
	nit_form=forms.ConsultaNit(request.form) #Captura los datos del formuario

	if request.method == 'POST' and nit_form.validate(): #Validate() ejecuta las reglas de validacion que se establecieron en forms.py
		nit=nit_form.nit.data

		#webservice_request(nit)
		#conn=connectionDB()
		#cursor = conn.cursor()
		save_dataframe(nit)


	return render_template('index.html', form=nit_form)

if __name__ == "__main__":
	app.run()