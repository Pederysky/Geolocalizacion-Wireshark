import pygeoip

def geo(fich_Datos_Localizacion,ip):
    #Generamos el objeto de Localizacion con los Datos del fichero
    geoDb = pygeoip.GeoIP(fich_Datos_Localizacion)
    ''' El metodo record_by_addr me devuelve la informacion
    de la IP '''
    print (geoDb.record_by_addr(ip))

def main( ip):
    ''' Podemos descargar la base de datos de Geolocalizacion 
    desde:https://dev.maxmind.com/geoip/legacy/geolite 
    Nosotros hemos bajado el básico pero existe ficheros más completos
    con mucha más informacion
    '''
    geo('GeoLiteCity.dat', ip)

if __name__ == "__main__":
    print ('Escaner de IP. Agradecimientos a http://www.flu-project.com\n')
    # dns de google
    main('8.8.8.8')