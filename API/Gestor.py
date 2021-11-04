import json
import os
from xml.etree.ElementTree import TreeBuilder
from _elementtree import *
import xml.etree.cElementTree as ET
from flask import *
from DocumentoTE import DocumentoTE
from tkinter import filedialog, Tk
from tkinter.filedialog import *
from tkinter import * 
from Aprobacion import Aprobacion 
from Autorizaciones import Autorizaciones
from Errores import Errores
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
                    NitEmisor= NitEmisor.replace('\n','')
                    try:
                        niit = self.ValidarNit(NitEmisor)
                        if niit == True:
                            ErrorNitE = False
                        else:
                            ErrorNitE = True
                    except:
                        ErrorNitE=True
                elif ele.tag == "NIT_RECEPTOR":
                    NitReceptor = ele.text
                    NitReceptor = NitReceptor.replace(' ','')
                    NitReceptor= NitReceptor.replace('\n','')
                    try:
                        niit = self.ValidarNit(NitReceptor)
                        if niit == True:
                            ErrorNitR = False
                        else:
                            ErrorNitR = True
                    except:
                        ErrorNitR=True
                elif ele.tag == "VALOR":
                    ErrorValor=False
                    Valor = ele.text
                    Valor =Valor.replace(' ','')
                    Valor =Valor.replace('\n','')
                    try:
                        Valor = round(float(Valor),2)
                    except:
                        ErrorValor=True
                elif ele.tag == "IVA":
                    Iva = ele.text
                    Iva =Iva.replace(' ','')
                    Iva =Iva.replace('\n','')
                    try:
                        if self.ValidarIva(Valor)==float(Iva):
                            ErrorIva = False
                        else:
                            ErrorIva=True
                    except:
                        ErrorIva=True
                elif ele.tag == "TOTAL":
                    Total = ele.text
                    try:
                        if self.ValidarTotal(Valor,float(Iva))==float(Total):
                            ErrorTotal=False
                        else:
                            ErrorTotal=True
                    except:
                        ErrorTotal=True
            esCorrecta = self.ValidarEsCorrecta(ErrorNitE,ErrorNitR, ErrorIva, ErrorTotal, ErrorValor)
            dteTemp.append(DocumentoTE(fecha, Referencia, NitEmisor, NitReceptor, Valor, Iva, Total, ErrorNitE, ErrorNitR, ErrorIva, ErrorTotal, esCorrecta))
            self.ListaDTE.append(dteTemp)
            dteTemp = []
    
    def ValidarIva(self, valor):
        iva = round(valor*0.12,2)
        return iva

    def ValidarEsCorrecta(self,ErrorNitE,ErrorNitR, ErrorIva, ErrorTotal, ErrorValor):
        if ErrorNitE==True or ErrorNitR==True or ErrorIva==True or ErrorTotal==True or ErrorValor==True:
            return False
        else:
            return True

    def ValidarTotal(self,valor, iva):
        return valor+iva

    def MostrarSalida(self):
        f=open('API\Salidas\salidaPrueba.xml')
        return Response(response=f.read(),mimetype='text/plain',content_type='text/plain')  
                    
    def ArchivoSalida(self):
        top =  ET.Element("LISTAAUTORIZACIONES")
        Autorizacion = ET.SubElement(top,"AUTORIZACION")
        for i in self.ListaSalidaAuto:
            fecha = ET.SubElement(Autorizacion,"FEHCA").text = i.Fecha
            Facturas_Recibidas = ET.SubElement(Autorizacion,'FACTURAS_RECIBIDAS').text=str(i.FacturasRecibidas)
            Errores = ET.SubElement(Autorizacion,'ERRORES')
            for j in i.Errores:
                E_NitE = ET.SubElement(Errores, 'NIT_EMISOR').text = str(j.ErrorNitE)
                ErrorNitR = ET.SubElement(Errores, 'NIT_RECEPTOR').text = str(j.ErrorNitR)
                ErrorIva = ET.SubElement(Errores, 'IVA').text = str(j.ErrorIva)
                ErrorTotal = ET.SubElement(Errores, 'TOTAL').text = str(j.ErrorTotal)
                ErrorReferencia = ET.SubElement(Errores, 'REFERENCIA_DUPLICADA').text = str(j.ErrorReferencia)
            Facturas_Correctas = ET.SubElement(Autorizacion,'FACTURAS_CORRECTAS').text= str(i.FacturasCorrectas)
            cantEmisores = ET.SubElement(Autorizacion,'CANTIDAD_EMISORES').text= str(i.cantEmisores)
            cantReceptores = ET.SubElement(Autorizacion,'CANTIDAD_RECEPTORES').text= str(i.cantReceptores)
            ListadoA = ET.SubElement(Autorizacion, 'LISTADO_AUTORIZACIONES')
            for n in i.Aprobaciones:
                Aprobacionees = ET.SubElement(ListadoA, "APROBACION")
                NitE = ET.SubElement(Aprobacionees,'NIT_EMISOR').text =str(n.nitE)
                CodigoAprobacion = ET.SubElement(Aprobacionees,'TOTAL').text = str(n.CodAprobacion)
        archivo = ET.ElementTree(top)
        archivo.write('API\Salidas\salidaPrueba.xml',encoding='utf-8',xml_declaration=True)
        
        
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
            suma+=mul
        suma-=int(v)
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
            for y in x:
                if y.Revisada==False:
                    fecha = y.tiempo
                    cantidadFacturas = self.CantidadFacturas(fecha)
                    FacturasCorrectas = self.CantFacturasCorrectas(fecha)
                    cantidadNitE = self.CantidadNitEC(fecha)
                    cantidadNitR = self.CantidadNitRC(fecha)
                    Erroress = self.ErroresListaDte(fecha)
                    Aprobaciones = self.Aprobaciones(fecha)
                self.ListaSalidaAuto.append(Autorizaciones(fecha, cantidadFacturas, Erroress, FacturasCorrectas, cantidadNitE, cantidadNitR, Aprobaciones ))       
                    

    def CantidadFacturas(self, fecha):
        contadorCantidadFacturas=0
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo == fecha:
                    contadorCantidadFacturas+=1
                    y.Revisada==True
        return contadorCantidadFacturas    

    def CantFacturasCorrectas(self, fecha):
        contadorCorrectas=0
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo == fecha:
                    if y.Correcta == True:
                        contadorCorrectas+=1
        return contadorCorrectas        

    def CantidadNitEC(self, fecha):
        contadorCantidadNitEC=0
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo == fecha:
                    if y.ErrorNitE==False:
                        contadorCantidadNitEC+=1
        return contadorCantidadNitEC

    def CantidadNitRC(self, fecha):
        contador=0
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo==fecha:
                    if y.ErrorNitR==False:
                        contador+=1
        return contador

    def ErroresListaDte(self, fecha):
        ErrorEmisor = 0
        ErrorReceptor = 0 
        ErrorIva = 0
        ErrorTotal = 0
        ErrorReferencia = 0
        ErrorEmisor = self.ErrorEmisores(fecha)
        ErrorReceptor = self.ErrorReceptores(fecha)
        ErrorIva= self.ErrorIva(fecha)
        ErrorTotal= self.ErrorTotal(fecha)
        err = []
        err.append(Errores(ErrorEmisor,ErrorReceptor, ErrorIva, ErrorTotal, ErrorReferencia))
        return err

    def ErrorEmisores(self, fecha):
        contador = 0 
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo==fecha:
                    if y.ErrorNitE==True:
                        contador+=1
        return contador
        
    #lista errores
    def ErrorReceptores(self,fecha):
        contador = 0 
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo==fecha:
                    if y.ErrorNitR==True:
                        contador+=1
        return contador

    def ErrorIva(self,fecha):
        contador = 0 
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo==fecha:
                    if y.ErrorIva==True:
                        contador+=1
        return contador

    def ErrorTotal(self, fecha):
        contador = 0 
        for x in self.ListaDTE:
            for y in x:
                if y.tiempo==fecha:
                    if y.ErrorTotal==True:
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
            for y in x:
                if y.tiempo==fecha:
                    if y.Correcta==True:
                        contador+=1
                        NitAprobado=y.nitE
                        referencia = y.referencia
                        codigoAprobacion=self.codigoAprobacion(fecha,contador)
                        aprobado.append(Aprobacion(NitAprobado,referencia,codigoAprobacion))
        return aprobado

    def codigoAprobacion(self, fecha,contador):
        codigo = fecha[6]+fecha[7]+fecha[8]+fecha[9]+fecha[3]+fecha[4]+fecha[0]+fecha[1]
        codigo+='00000000'
        codigo= int(codigo)
        return codigo+contador
        codigo = fecha[6]+fecha[7]+fecha[8]+fecha[9]+fecha[3]+fecha[4]+fecha[0]+fecha[1]
        codigo+='00000000'
        codigo= int(codigo)
        return codigo+contador

    def AyudaDatosEstudiante(self):
        datos = '{"Nombre":"Carlos Augusto calderon estrada", "carné":"201905515", "Curso":"IPC2", "Seccion":"D"}'
        
        return datos

    def openEnsayo(self):
        os.startfile('API\Documentacion\Ensayo.pdf')
