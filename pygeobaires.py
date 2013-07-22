
# esto:
# http://ws.usig.buenosaires.gob.ar/geocoder/2.2

from urllib import urlencode
from urllib2 import urlopen
import json
import re

class GeoBaires:
    @property
    def url(self):
        return 'http://ws.usig.buenosaires.gob.ar/geocoder/2.2/geocoding?%s'
    
    @property
    def url_conversor(self):
        return 'http://ws.usig.buenosaires.gob.ar/rest/convertir_coordenadas?%s'
    
         
    def to_lat_long(self, x, y):
        params = {
            'x': x,
            'y': y,
            'output': 'lonlat'
        }

        url = self.url_conversor % urlencode(params)
        page = urlopen(url)
        
        res = json.loads(page.read())
        
        if res['tipo_resultado'] == 'Ok':
            return res['resultado']['x'], res['resultado']['y']
        
        
    def geocode_split(self, address, number):
        params = {
            'cod_calle': address,
            'altura': number,
        }
           
        url = self.url % urlencode(params)
        page = urlopen(url)
        
        to_parse = re.findall('\((.*)\)', page.read())[0]
        
        coord = json.loads(to_parse)
        
        return self.to_lat_long(coord['y'], coord['x']) 
        
        
    def geocode(self, address):
        if isinstance(address, unicode):
            address = address.encode('utf-8')
        
        parts = re.match('(.*)\s+(\d+$)', address).groups()
        
        return self.geocode_split(parts[0], parts[1])
