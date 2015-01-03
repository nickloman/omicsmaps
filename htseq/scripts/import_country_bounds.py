
from htseq.centres.models import Country
import sys

for ln in sys.stdin:
    cols = ln.rstrip().split(",")
    try:
        c = Country.objects.get(name = cols[4])
        c.sw_lat = cols[1]
        c.sw_long = cols[0]
        c.ne_lat = cols[3]
        c.ne_long = cols[2]
        c.save()
    except Country.DoesNotExist, e:
        print "Skipping %s" % (cols[4],)

