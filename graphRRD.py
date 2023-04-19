import sys
import rrdtool
import time

def Imagenes(tiempo_inicial, tiempo_final):
    rrdtool.graph( "traficoMulticast.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Bytes/s",
                         "--title=Paquetes unicast que ha recibido \n la interfaz de red de un agente",
                         "DEF:traficoEntrada=trafico.rrd:Mul:AVERAGE",
                         "CDEF:escalaIn=traficoEntrada,8,*",
                         "LINE1:escalaIn#0000FF:Paquetes unicast recibidos")

    rrdtool.graph( "traficoIP.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Bytes/s",
                         "--title=Paquetes recibidos \n a protocolos IP",
                         "DEF:traficoEntrada=trafico.rrd:IP:AVERAGE",
                         "CDEF:escalaIn=traficoEntrada,8,*",
                         "LINE1:escalaIn#0000FF:Paquetes IP recibidos")

    rrdtool.graph( "traficoICMP.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Bytes/s",
                         "--title=Mensajes ICMP echo \n que ha enviado el agente",
                         "DEF:traficoEntrada=trafico.rrd:ICMP:AVERAGE",
                         "CDEF:escalaIn=traficoEntrada,8,*",
                         "LINE1:escalaIn#0000FF:Mensajes ICMP echo")

    rrdtool.graph( "traficoEnviados.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Bytes/s",
                         "--title=Segmentos recibidos que incluyen los \n con errores",
                         "DEF:traficoEntrada=trafico.rrd:Enviados:AVERAGE",
                         "CDEF:escalaIn=traficoEntrada,8,*",
                         "LINE1:escalaIn#0000FF:Segmentos recibidos")

    rrdtool.graph( "traficoDatagramas.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Bytes/s",
                         "--title=Datagramas UDP entregados \n a usuarios ",
                         "DEF:traficoEntrada=trafico.rrd:Datagramas:AVERAGE",
                         "CDEF:escalaIn=traficoEntrada,8,*",
                         "LINE1:escalaIn#0000FF:Datagramas UDP")