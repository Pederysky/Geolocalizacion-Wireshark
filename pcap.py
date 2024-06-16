#lo utilizaremos para poder leer paquetes de red
#pip install dpkt
import dpkt 
#sus utilidades son multiples, pero en este caso sólo para una conversion
import socket 
#Librería que al pasarle una IP me devuelve informacion geografica de la misma
#pip install pygeoip
import pygeoip

import json

ETH_TYPE_IP = 0x0800  # Si es IP protocol
gi = pygeoip.GeoIP('GeoLiteCity.dat')


def main():
    try:
        listaDatos=[]
        with open('record.pcap', 'rb')  as f:
            pcap = dpkt.pcap.Reader(f)
    
            #Generaremos un archivo KML
            #Un archivo KML no es más que un archivo XML compatibles con Maps de Google
            kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
            '<Style id="transBluePoly">' \
                        '<LineStyle>' \
                        '<width>1.5</width>' \
                        '<color>501400E6</color>' \
                        '</LineStyle>' \
                        '</Style>'
            kmlfooter = '</Document>\n</kml>\n'
            kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
                   

            #print(kmldoc)
        with open ('resultado.kml','w') as f:
            f.write(kmldoc)

    except :
        print ("Se han producido errores al ejecutar el código")

      
def plotIPs(pcap):
    '''Leemos el fichero pcap y lo recorremos de manera que obtenemos informacion
    de sus IP y a la vez con dichas IP obtenemos sus datos de posicionamiento GPS
    '''
    kmlPts = ''
    listaDatos=[]
    for (ts, buf) in pcap:
        try:
            Direccion={}
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type==ETH_TYPE_IP:#peticion de tipo IP
                ip = eth.data
                #convierto la direccion a un formato legible
                src = socket.inet_ntoa(ip.src)
                dst = socket.inet_ntoa(ip.dst)

                KML, datoPosicion = retKML(dst, src)
                kmlPts = kmlPts + KML
                listaDatos.append(datoPosicion)

               
        except:
            pass
    with open ('resultado.json','w') as f:
        json.dump(listaDatos,f)
    return kmlPts 


                    
    

def retKML(dstip, srcip):
    '''
    Obtenemos para cada petición ip los datos de posicionamientos GPS
    y lo convertimos a registro XML
    con el formato KML
    '''
    Direccion={}
    #Saco información de destino
    dst = gi.record_by_name(dstip)
    #información de mi maquina publica
    src = gi.record_by_name('83.36.10.85')
    Direccion["ip_origen"]=src
    Direccion["ip_destion"]=dst

    #esta la cojo a "mano" usad esta pues es con la que hemos creado los datos
    #podríamos cogerla, pero sería complicar el ejemplo más
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml, Direccion
    except:
        return '',{}


if __name__ == '__main__':
    main()