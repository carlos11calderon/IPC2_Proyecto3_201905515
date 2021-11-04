from flask import *
from flask_cors import CORS

from Gestor import *


app = Flask(__name__)
app.config["DEBUG"] = True

gestor = Gestor()
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return 'SERVER IS WORKING!!!!'

@app.route('/ConsultaDatos', methods=['GET'])
def ObtenerDatos():
    return gestor.MostrarSalida()

@app.route("/nxml", methods=['GET'])
def nombre_xml():
    global nom
    nom = request.data
    return nom

@app.route('/Procesar', methods=['GET'])
def Procesar():
    gestor.salidaAuto()
    gestor.ArchivoSalida()
    return '{"data":"Listo para mostrar"}'

@app.route('/Ayuda', methods=['GET'])
def Ayuda():
    gestor.openEnsayo()
    return gestor.AyudaDatosEstudiante()

@app.route('/SubirXml', methods=['POST'])
def prueba():
    xml_data = request.data
    archivo_xml = open("API\pr.xml", "wb")
    #archivo_xml2 = open("frontend\ frontent\pr.xml", "wb")
    archivo_xml.write(xml_data)
    archivo_xml.close()
    gestor.AbrirArchivo()
    return Response(xml_data, mimetype='text/xml')

# END POINTS

#Iniciamos el servidor

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True )