from flask import *
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True


CORS(app)

@app.route('/', methods=['GET'])
def home():
    return 'SERVER IS WORKING!!!!'

@app.route('/ConsultaDatos', methods=['GET'])
def ObtenerDatos():
    pass

@app.route('/ResumenIva', methods=['GET'])
def ObtenerResumenIva():
    pass

@app.route('/ResumenRango', methods=['GET'])
def ObtenerResumenRango():
    pass

@app.route('/Grafica', methods=['GET'])
def ObtenerGrafica():
    pass

@app.route('/Procesar', methods=['POST'])
def CrearProceso():
    pass

# END POINTS

#Iniciamos el servidor

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)