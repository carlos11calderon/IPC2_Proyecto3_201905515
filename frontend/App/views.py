from django.shortcuts import render
import requests
# Create your views here.

endpoint = 'http://192.168.1.15:5000/'



def home(request):
    global nom
    enxml = ""
    l=""
    cont=0
    context={}
    if request.method == 'POST':
        archivo_subido= request.FILES['Cargar_archivo']
        nom=archivo_subido.name
        xmlinicio = open(nom, "r")
        for linea in xmlinicio:
            enxml=str(enxml)+str(linea)
        context['todoxml'] = enxml

        #------------- PARA ENVIAR EL XML DESDE FRONT A BACK-----------------

        archivo_xml = open(nom, "r")
        lectura_xml = archivo_xml.read()
        # HACE LA CONSULTA ENVIANDO EL ARCHIVO XML
        r = requests.get(endpoint+'SubirXml',data=lectura_xml)
        n = requests.get(endpoint+'', data=nom)


    return render(request,'index.html',context)

def obtenerXML(request):
    global nom
    enxml = ""
    enxmli = ""
    l = ""
    cont = 0
    context = {}
    context2 = {}
    if request.method == 'GET':
        archivo_xmls=open("Archivo.xml","w")
        r = requests.get(endpoint+'/ConsultaDatos')
        archivo_xmls.write(r.text)
        archivo_xmls.close()

        xmlfinal = open("Archivo.xml","r")

        for linea in xmlfinal:
            enxml = str(enxml) + str(linea)
        context2['todoxml2'] = enxml

        xmlinicio = open(nom, "r")
        for line in xmlinicio:
            enxmli = str(enxmli) + str(line)
        context['todoxml'] = enxmli

    return render(request, 'index.html', context2)