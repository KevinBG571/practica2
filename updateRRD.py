import time
import rrdtool
from getSNMP import consultaSNMP

def crear():
    ret = rrdtool.create("trafico.rrd",
                         "--start", 'N',
                         "--step", '60',
                         "DS:Mul:COUNTER:120:U:U",
                         "DS:IP:COUNTER:120:U:U",
                         "DS:ICMP:COUNTER:120:U:U",
                         "DS:Enviados:COUNTER:120:U:U",
                         "DS:Datagramas:COUNTER:120:U:U",
                         "RRA:AVERAGE:0.5:5:5",
                         #"RRA:AVERAGE:0.5:1:1400"
                         )

    if ret:
        print(rrdtool.error())

    rrdtool.dump("trafico.rrd", "trafico.xml")

def update(comunidad,host,interfaz):
    while 1:
        dato1 = int(consultaSNMP(comunidad,host,
                                                '1.3.6.1.2.1.2.2.1.11.'+interfaz))

        dato2 = int(consultaSNMP(comunidad,host,
                                                '1.3.6.1.2.1.4.3.0'))

        dato3 = int(consultaSNMP(comunidad,host,
                                                '1.3.6.1.2.1.5.8.0'))

        dato4 = int(consultaSNMP(comunidad,host,
                                                '1.3.6.1.2.1.6.10.0'))

        dato5 = int(consultaSNMP(comunidad,host,
                                                '1.3.6.1.2.1.7.1.0'))
        valor = "N:" + str(dato1) +':'+str(dato2)+':'+str(dato3)+':'+str(dato4)+':'+str(dato5)
        rrdtool.update('trafico.rrd', valor)
        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)