import datetime

from getSNMP import consultaSNMP
from getSNMP import cambiarSNMP
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak
from reportlab.lib import colors
from reportlab.platypus import Image
from updateRRD import crear
from updateRRD import update
from graphRRD import Imagenes
import multiprocessing
def Agregar():
    archivo = open("bdd.txt", "r")
    inf = archivo.readlines()
    archivo2 = open("bdd.txt", "w")
    for i in range(len(inf)):
        linea = str(i) + inf[i][1:]
        archivo2.write(linea)
    comunidad = input("Comunidad: ")
    version = input("Versiòn SNMP: ")
    puerto = input("Puerto: ")
    ip = input("IP: ")
    archivo2.write(str(len(inf))+'-')
    archivo2.write(comunidad + ',')
    archivo2.write(version + ',')
    archivo2.write(puerto + ',')
    archivo2.write(ip + '\n')
    archivo2.close()
    archivo.close()

def Cambiar():
    archivo = open("bdd.txt", "r")
    inf = archivo.readlines()
    print(inf)
    agente = input("Selecciona un agente a modificar: ")
    archivo2 = open("bdd.txt", "w")

    for linea in inf:
        if linea[0] == agente:
            opcion = linea.split("-")
            partes = opcion[1].split(",")
            comunidad = input("Comunidad: ")
            version = input("Versiòn SNMP: ")
            puerto = input("Puerto: ")
            ip = input("IP: ")
            archivo2.write(linea[0] + '-')
            archivo2.write(comunidad + ',')
            archivo2.write(version + ',')
            archivo2.write(puerto + ',')
            archivo2.write(ip + '\n')
            if partes[0] != comunidad:
                cambiarSNMP(partes[0],ip,comunidad)
        else:
            archivo2.write(linea)
    archivo.close()
    archivo2.close()



def Eliminar():
    archivo = open("bdd.txt", "r")
    inf = archivo.readlines()
    print(inf)
    agente = input("Elige un agente: ")
    archivo2 = open("bdd.txt", "w")
    for linea in inf:
        if linea[0] != agente:
            archivo2.write(linea)
    archivo.close()
    archivo2.close()
    archivo = open("bdd.txt", "r")
    inf = archivo.readlines()
    archivo2 = open("bdd.txt", "w")
    for i in range(len(inf)):
        linea = str(i) + inf[i][1:]
        archivo2.write(linea)


def Reporte():
    estados = {" 1": "Up", " 2": "Down", " 3": "Testing", " 4": "Unknown", " 5": "Dormant", " 6": "NotPresent",
               "7": "LoweLayerDown"}
    archivo = open("bdd.txt", "r")
    informacion = archivo.read()
    print(informacion)
    lista = informacion.split("\n")
    agente = input("Elige un agente: ")
    for i in range(len(lista)):
        opcion = lista[i].split("-")
        if opcion[0] == agente:
            partes = opcion[1].split(",")
            pdf = canvas.Canvas("REPORTESNMP.pdf")
            pdf.drawString(70, 750, "Administraciòn de Servicios en Red")
            pdf.drawString(70, 710, "Practica 1")
            pdf.drawString(70, 670, "Baldovinos Gutierrez Kevin 4CM14")

            SO = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.1.1.0').split("-")
            nombre = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.1.5.0')
            contacto = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.1.4.0')
            ubicacion = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.1.6.0')
            interfaces = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.2.1.0')
            pdf.drawString(56, 600, SO[0])
            pdf.drawString(56, 580, SO[1])
            if " Windows" in SO[0] or " Windows" in SO[1]:
                pdf.drawImage("Windows.jpeg", 400, 450, width=100, height=100)
            else:
                pdf.drawImage("Ubuntu.jpg", 390, 450, width=200, height=160)

            pdf.drawString(70, 560, "Nombre del dispositivo: "+nombre)
            pdf.drawString(70, 540, "Informacion de contacto: "+contacto)
            pdf.drawString(70, 520, "Ubicacion: "+ubicacion)
            pdf.drawString(70, 500, "Numero de interfaces: "+interfaces)
            print()
            print("------------------------------------------------------")
            print()
            datos = [["Interfaces activas","Estado"]]
            if int(interfaces) > 5:
                for i in range(1, 6):
                    desc = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.2.2.1.2.'+str(i))
                    estado = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.2.2.1.7.'+str(i))
                    datos.append((desc, estados[estado]))
            else:
                for i in range(1,int(interfaces)+1):
                    desc = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.2.2.1.2.' + str(i))
                    estado = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.2.2.1.7.' + str(i))
                    datos.append((desc, estados[estado]))

            tabla = Table(datos)
            
            tabla.wrapOn(pdf, 0, 0)
            tabla.drawOn(pdf, 60, 250)
            pdf.save()
            break
    archivo.close
def Update():
    crear()
    archivo = open("bdd.txt", "r")
    informacion = archivo.read()
    print(informacion)
    lista = informacion.split("\n")
    print()
    agente = input("Agente a analizar: ")
    interfaz = input("Ingresa la interfaz: ")
    for i in range(len(lista)):
        opcion = lista[i].split("-")
        if opcion[0] == agente:
            partes = opcion[1].split(",")
            p = multiprocessing.Process(target=update, args=(partes[0], partes[3],interfaz))
            p.start()
            break
    archivo.close
    return agente
def Contabilidad(agente):
    print(agente)
    archivo = open("bdd.txt", "r")
    informacion = archivo.read()
    lista = informacion.split("\n")
    print("AAAA-MM-DD HH:MM:SS")
    inicial = input("Fecha inicial: ")
    final = input("Fecha final: ")
    for i in range(len(lista)):
        opcion = lista[i].split("-")
        if opcion[0] == agente:

            partes = opcion[1].split(",")
            pdf = canvas.Canvas("REPORTECONTABILIDAD.pdf")

            pdf.drawString(75, 750, "Administraciòn de Servicios en Red")
            pdf.drawString(75, 710, "Práctica 2")
            pdf.drawString(75, 670, "Baldovinos Gutiérrez Kevin 4CM14")

            SO = consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.1.1.0').split("-")
            
            pdf.drawString(56, 580, "device: " + consultaSNMP(partes[0], partes[3], '1.3.6.1.2.1.1.5.0'))
            pdf.drawString(56, 560, "description: " + SO[0])
            pdf.drawString(120, 540, SO[1])
            pdf.drawString(56, 520, "date: " + inicial)
            pdf.drawString(56, 500, "rdate: " + final)

            Imagenes(int(datetime.datetime.strptime(inicial, '%Y-%m-%d %H:%M:%S').timestamp()), int(datetime.datetime.strptime(final, '%Y-%m-%d %H:%M:%S').timestamp()))

            pdf.drawString(90, 450, "1.1 Paquetes unicast que ha recibido una interfaz de red de un agente")
            pdf.drawImage("traficoMulticast.png",56,250)
            pdf.drawString(90, 230, "1.2 Paquetes recibidos a protocolos IP, incluyendo los que tienen errores")
            pdf.drawImage("traficoIP.png", 56, 30)
            pdf.showPage()
            pdf.drawString(90, 750, "1.3 Mensajes ICMP echo que ha enviado el agente")
            pdf.drawImage("traficoICMP.png", 56, 550)
            pdf.drawString(90, 530, "1.4 Segmentos recibidos, incluyendo los que se han recibido con errore")
            pdf.drawImage("traficoEnviados.png", 56, 330)
            pdf.drawString(90, 310, "1.5 Datagramas entregados a usuarios UDP")
            pdf.drawImage("traficoDatagramas.png", 56, 110)
            pdf.save()
            break
        if agente is None:
            print("Se tiene que activar primero el analizador\n")
            break
    archivo.close

opciones = {"1": Agregar, "2": Cambiar, "3": Eliminar, "4": Reporte, "5":Update , "6": Contabilidad}
agente = None
while 1:
    print("************************************************* \n"
          "\t Sistema de administración de red \n"
          "Practica 2 -Módulo de administración de contabilidad \n "
          "Baldovinos Gutiérrez Kevin 4CM14 2020630037 \n"
          "************************************************* \n"
          "\n"
          "Elige una opciòn: \n"
          "1) Agregar dispositivo\n"
          "2) Cambiar informacion de dispositivo\n"
          "3) Eliminar informacion de dispositivo\n"
          "4) Generar reporte 1\n"
          "5) Iniciar monitoreo \n"
          "6) Reporte de contabilidad\n")

    elegir = input("")
    if elegir in opciones:
        if elegir == '5':
            agente = opciones[elegir]()
        elif elegir == '6':
            opciones[elegir](agente)
        else:
            opciones[elegir]()
    else:
        print("Opcion invalida")
