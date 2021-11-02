import json
from _elementtree import *
import xml.etree.cElementTree as ET
from flask import *
from DocumentoTE import DocumentoTE
from tkinter import filedialog, Tk
from tkinter.filedialog import *
from tkinter import * 
class Gestor:
    def __init__(self):
        self.ListaDTE = []

    def AbrirArchivo(self):
        ruta = 'API\pr.xml'
        tree = ET.parse(ruta)
        root = tree.getroot()
        ## Objeto de la lista de Lineas
        dteTemp=[]
        for elemento in root:
            print(elemento)
            ##for para listas de produccion
            for ele in elemento:
                if ele.tag == "TIEMPO":
                    Tiempo = ele.text
                elif ele.tag == "REFERENCIA":
                    Referencia = ele.text
                elif ele.tag == "NIT_EMISOR":
                    NitEmisor = ele.text
                elif ele.tag == "NIT_RECEPTOR":
                    NitReceptor = ele.text
                elif ele.tag == "VALOR":
                    Valor = ele.text
                elif ele.tag == "IVA":
                    Iva = ele.text
                elif ele.tag == "TOTAL":
                    Total = ele.text
            dteTemp.append(DocumentoTE(Tiempo, Referencia, NitEmisor, NitReceptor, Valor, Iva, Total))
            self.ListaDTE.append(dteTemp)
            dteTemp = []
        
            
    def MostrarSalida(self):
        f=open('salidaPrueba.xml')
        return Response(response=f.read(),mimetype='text/plain',content_type='text/plain')  
                    
    def ArchivoSalida(self):
        top =  ET.Element("SalidaPrueba")
        for i in self.ListaDTE:
            Dtee = ET.SubElement(top,"DTE")
            for j in i:
                tiempo = ET.SubElement(Dtee,'TIEMPO').text=j.tiempo
                referencia = ET.SubElement(Dtee,'REFERENCIA').text = j.referencia
                nitEmisor = ET.SubElement(Dtee,'NIT_EMISOR').text=j.nitE
                nitReceptor = ET.SubElement(Dtee,'NIT_RECEPTOR').text=j.nitR
                valor = ET.SubElement(Dtee,'VALOR').text=j.valor
                iva = ET.SubElement(Dtee,'IVA').text=j.iva
                total = ET.SubElement(Dtee,'TOTAL').text = j.total
        archivo = ET.ElementTree(top)
        archivo.write('salidaPrueba.xml')
        

    def ValidarNit(self, nit):
        suma=0
        tam = len(nit)
        v = nit[tam-1]
        
        for x in range(len(nit)):
            mul=0
            mul = int(nit[x])*tam
            tam-=1
            suma+=mul
        print(suma)
        modular = suma%11
        resultado1 = 11-modular
        k = resultado1%11

        print(modular)
        print('k es: '+str(k))
        print('v es: '+v)
        if k<10 and k == v :
            return '{"data":"Valido"}'
        elif k >=10 or k!=v:
            return '{"data":"invalido"}'
        else: 
            return '{"Estado":"Algo malo paso"}'