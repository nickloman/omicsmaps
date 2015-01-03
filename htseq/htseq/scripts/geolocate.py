from htseq.centres.models import Centre, CentreCapacity, Platform, Country
from django.conf import settings
import json
from urllib import urlopen
import pprint
import sys

url = "http://maps.google.com/maps/geo?q=%s,%s&output=json&sensor=false&key=" + settings.GOOGLE_API_KEY

for c in Centre.objects.filter(country=None):
    o = json.load(urlopen(url % (c.lat, c.long)))
    for p in o['Placemark']:
        print "placemark: %s" % (p,)

        try:
            country_name = p['AddressDetails']['Country']['CountryName']
            country_code = p['AddressDetails']['Country']['CountryNameCode']
        except KeyError:
            continue

        try:
            admin_area = p['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        except KeyError:
            admin_area = c.locality

        print >>sys.stderr, admin_area, country_name, country_code
        country, was_created = Country.objects.get_or_create(name = country_name, country_code = country_code)
        c.country = country

        c.locality = admin_area

        c.save()
        print "Success"
        break

