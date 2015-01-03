from django.conf import settings
import json
from urllib import urlopen

def geolocate(lat, lon):
    url = "http://maps.google.com/maps/geo?q=%s,%s&output=json&sensor=false&key=" + settings.GOOGLE_API_KEY
    o = json.load(urlopen(url % (lat, lon)))
    for p in o['Placemark']:
        try:
            country_name = p['AddressDetails']['Country']['CountryName']
            country_code = p['AddressDetails']['Country']['CountryNameCode']
        except KeyError:
            continue

        try:
            admin_area = p['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        except KeyError:
            admin_area = ''

        return country_name, country_code, admin_area
    raise ValueError

