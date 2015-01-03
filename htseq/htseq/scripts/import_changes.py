from htseq.centres.models import Centre, Country
from htseq.centres.geolocate import geolocate

import sys

for ln in sys.stdin:
    cols = ln.rstrip().split("\t")
    long, lat, trash = cols[4].split(",")

    o = Centre.objects.filter(long = long).filter(lat = lat)
    if not o:
        if cols[0].startswith('Placemark'):
            continue

        try:
            c = Centre.objects.get(name = cols[0])
        except Centre.DoesNotExist:
            c = Centre()
            c.name = cols[0]
            c.url = cols[3]
            c.notes = cols[1]
            c.lat = lat
            c.long = long
       
            try:
                country_name, country_code, locality = geolocate(c.lat, c.long)
                c.country = Country.objects.get(country_code = country_code)
                c.locality = locality

                c.save()
            except ValueError, e:
                print cols
            except KeyError, e:
                print cols

