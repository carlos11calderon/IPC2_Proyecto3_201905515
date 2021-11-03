import json
from os import error, truncate
from xml.etree.ElementTree import TreeBuilder
from _elementtree import *
import xml.etree.cElementTree as ET
from flask import *
from DocumentoTE import DocumentoTE
from tkinter import filedialog, Tk
from tkinter.filedialog import *
from tkinter import * 
import Aprobacion, Autorizaciones, Errores
class Gestor:
    def __init__(self):
        self.ListaDTE = []
        self.ListaSalidaAuto=[]

    def AbrirArchivo(self):
        ruta = 'API\pr.xml'
        tree = ET.parse(ruta)
        root = tree.getroot()
        ## Objeto de la lista de Lineas
        dteTemp=[]
        for elemento in root:
            ##for para listas de produccion
            for ele in elemento:
                if ele.tag == "TIEMPO":
                    Tiempo = ele.text
                    fecha = self.automataFecha(Tiempo)
                elif ele.tag == "REFERENCIA":
                    Referencia = ele.text
                elif ele.tag == "NIT_EMISOR":
                    NitEmisor = ele.text
                    NitEmisor= NitEmisor.replace(' ','')
                    niit = self.ValidarNit(NitEmisor)
                    if niit == True:
                        ErrorNitE = False
                    else:
                        ErrorNitE = True
                elif ele.tag == "NIT_RECEPTOR":
                    NitReceptor = ele.text
                    NitReceptor = NitReceptor.replace(' ','')
                    niit = self.ValidarNit(NitReceptor)
                    if niit == True:
                        ErrorNitR = False
                    else:
                        ErrorNitR = True
                elif ele.tag == "VALOR":
                    Valor = ele.text
                    Valor = round(int(Valor),2)
                elif ele.tag == "IVA":
                    Iva = ele.text
                    if self.validarIva(Valor)==float(Iva):
                        ErrorIva = False
                    else:
                        ErrorIva=True
                elif ele.tag == "TOTAL":
                    Total = ele.text
                    if self.validarTotal(Valor,float(Iva))==float(Total):
                        ErrorTotal=False
                    else:
                        ErrorTotal=True
            esCorrecta = self.ValidarEsCorrecta(ErrorNitE,ErrorNitR, ErrorIva, ErrorTotal)
            dteTemp.append(DocumentoTE(fecha, Referencia, NitEmisor, NitReceptor, Valor, Iva, Total, ErrorNitE, ErrorNitR, ErrorIva, ErrorTotal, esCorrecta))
            self.ListaDTE.append(dteTemp)
            dteTemp = []
    
    def ValidarIva(self, valor):
        iva = round(valor*0.12,2)
        return iva

    def ValidarEsCorrecta(ErrorNitE,ErrorNitR, ErrorIva, ErrorTotal):
        if ErrorNitE==True or ErrorNitR==True or ErrorIva==True or ErrorTotal==True:
            return False
        else:
            return True

    def ValidarTotal(self,valor, iva):
        return valor+iva

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
        
    def isNumero(self,caracter):##metodo que retorna si es un digito
        if ((ord(caracter) >= 48 and ord(caracter) <= 57)):
            return True
        else:
            return False

    def automataFecha(self, tiempo):
        fecha=''
        estado=0

        for x in tiempo:
            if estado == 0 :
                if x == ',':
                    estado=1
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==1:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=2
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==2:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=3
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==3:
                if x=='/':
                    fecha+=x
                    estado=4
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==4:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=5
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==5:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=6
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==6:
                if x=='/':
                    fecha+=x
                    estado=7
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==7:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=8
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==8:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=9
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==9:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=10
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==10:
                if self.isNumero(x)==True:
                    fecha+=x
                    estado=11
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif estado==11:
                if ord(x)==32:
                    return fecha 

    def ValidarNit(self, nit):
        suma=0
        tam = len(nit)
        v = nit[tam-1]
        for x in range(len(nit)):
            mul=0
            mul = int(nit[x])*tam
            tam-=1
            if tam ==1:
                break 
            suma+=mul
        print(suma)
        modular = suma%11
        resultado1 = 11-modular
        k = resultado1%11

        print(modular)
        print('k es: '+str(k))
        print('v es: '+v)
        if k<10 and k == int(v) :
            return True
        elif k >=10 or k!=v:
            return False
        else: 
            return False

    def salidaAuto(self):
        cantidadFacturas=0
        Errores=[]
        FacturasCorrectas=0
        cantidadNitE=0
        cantidadNitR=0
        Aprobaciones=[]
        for x in self.ListaDTE:
            if x.Revisado==False:
                fecha = x.tiempo
                cantidadFacturas = self.CantidadFacturas(fecha)
                FacturasCorrectas = self.CantFacturasCorrectas(fecha)
                cantidadNitE = self.CantidadNitEC(fecha)
                cantidadNitR = self.CantidadNitRC(fecha)
                Errores = self.ErroresListaDte(fecha)
                Aprobaciones = self.Aprobaciones(fecha)
                

    def CantidadFacturas(self, fecha):
        contadorCantidadFacturas=0
        for x in self.ListaDTE:
            if x.tiempo == fecha:
                contadorCantidadFacturas+=1
                x.Revisado==True
        return contadorCantidadFacturas    

    def CantFacturasCorrectas(self, fecha):
        contadorCorrectas=0
        for x in self.ListaDTE:
            if x.tiempo == fecha:
                if x.esCorrecta == True:
                    contadorCorrectas+=1
        return contadorCorrectas        

    def CantidadNitEC(self, fecha):
        contadorCantidadNitEC=0
        for x in self.ListaDTE:
            if x.tiempo == fecha:
                if x.ErrorNitE==False:
                    contadorCantidadNitEC+=1
        return contadorCantidadNitEC

    def CantidadNitRC(self, fecha):
        contador=0
        for x in self.ListaDTE:
            if x.tiempo==fecha:
                if x.ErrorNitR==False:
                    contador+=1
        return contador

    def ErroresListaDte(self, fecha):
        errores = []
        ErrorEmisor = 0
        ErrorReceptor = 0 
        ErrorIva = 0
        ErrorTotal = 0
        ErrorReferencia = 0
        ErrorEmisor = self.ErrorEmisores(fecha)
        ErrorReceptor = self.ErrorReceptores(fecha)
        ErrorIva= self.ErrorIva(fecha)
        ErrorTotal= self.ErrorTotal(fecha)
        errores.append(Errores(ErrorEmisor,ErrorReceptor, ErrorIva, ErrorTotal, ErrorReferencia))
        return errores

    def ErrorEmisores(self, fecha):
        contador = 0 
        for x in self.ListaDTE:
            if x.tiempo==fecha:
                if x.ErrorNitE==True:
                    contador+=1
        return contador
        
    #lista errores
    def ErrorReceptores(self,fecha):
        contador = 0 
        for x in self.ListaDTE:
            if x.tiempo==fecha:
                if x.ErrorNitR==True:
                    contador+=1
        return contador

    def ErrorIva(self,fecha):
        contador = 0 
        for x in self.ListaDTE:
            if x.tiempo==fecha:
                if x.ErrorIva==True:
                    contador+=1
        return contador

    def ErrorTotal(self, fecha):
        contador = 0 
        for x in self.ListaDTE:
            if x.tiempo==fecha:
                if x.ErrorTotal==True:
                    contador+=1
        return contador

    def ErrorReferencia(self,fecha):
        return 0

    #lista aprobaciones

    def Aprobaciones(self, fecha):
        NitAprobado=''
        codigoAprobacion=''
        aprobado=[]
        contador=0
        for x in self.ListaDTE:
            if x.tiempo==fecha:
                if x.esCorrecta==True:
                    contador+=1
                    NitAprobado=x.NitE
                    referencia = x.referencia
                    codigoAprobacion=self.codigoAprobacion(fecha,contador)
                    aprobado.append(Aprobacion(NitAprobado,referencia,codigoAprobacion))
        return aprobado

    def codigoAprobacion(self, fecha,contador):
        codigo = fecha[6]+fecha[7]+fecha[8]+fecha[9]+fecha[3]+fecha[4]+fecha[0]+fecha[1]
        codigo+='00000000'
        codigo= int(codigo)
        return codigo+contador