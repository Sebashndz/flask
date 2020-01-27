from zeep import Client
import os
import codecs	

Directorio = os.getcwd() + "\\"
PathCarpetaConsultas = Directorio +"Python_Flask\\envDivisa\\Consultas\\"
PathArchivoNIT = Directorio +"ListaNIT_Fin.txt"


def CrearXML(NIT, Directorio, PathCarpetaConsultas):
	wsdl = "https://www.informacolombia.com/InformaIntWeb/services/ProductoXML?wsdl"
	client = Client(wsdl)
	#response = client.service.obtenerProductoXMLUncoded(**request_data)

	stringxml = """
	    <PETICION_PRODUCTO>
			<IDENTIFICACION>
			<USUARIO>C16134</USUARIO>
	                <PASSWORD>Infor48925</PASSWORD>
			</IDENTIFICACION>
			<USUARIO_ORIGEN>Equipo_BI</USUARIO_ORIGEN>
			<PRODUCTO>
			<NOMBRE>INFORME_FINANCIERO_INTERNACIONAL_XML</NOMBRE>
			<IDENTIFICADOR>{}</IDENTIFICADOR>
			<IDIOMA>01</IDIOMA>
			</PRODUCTO>
			<PROVINCIA>11</PROVINCIA>
			<LOCALIDAD>BOGOTA</LOCALIDAD>
			<CODPOSTAL>0511</CODPOSTAL>
	</PETICION_PRODUCTO>""".format(NIT)

	response = client.service.obtenerProductoXMLUncoded(stringxml)
	print(response)

	print("copiando el archivo-----------")


	if not os.path.exists(PathCarpetaConsultas):
	        os.makedirs(PathCarpetaConsultas)
	        print("Carpeta Creada")

	#with open(PathCarpetaConsultas + NIT + ".xml", 'w') as f:
	    #f.write(response)

	#with open(PathCarpetaConsultas + NIT + ".xml", 'w') as f:
    #f.write(response)


	with codecs.open(PathCarpetaConsultas + NIT + ".xml", 'w', encoding='latin-1') as f:
	    f.write(response)

	return	print("XML Creado: " + NIT)


#Se lee el archivo ListaNIT.txt linea por linea 
#y se consulta cada NIT.
def Iterar_Lista(PathArchivoNIT):
	f = open(PathArchivoNIT,'r').read().split('\n')
	for line in f:
	   	NIT = line
	   	print(NIT)
	   	CrearXML(NIT, Directorio, PathCarpetaConsultas)
	return True


#NIT2 = str(8909001619) #Familia
#NIT2 = str(8002497049) #COLWAGEN
#NIT2 = str(8909143141) #CONFECCIONES PORKY
#NIT2 = str(8909295023) #INDUSTRIA ALIMENTICIAS LA REI


#CrearXML(NIT2, Directorio, PathCarpetaConsultas)
Iterar_Lista(PathArchivoNIT)