
from htseq.centres.models import Country
import sys

for ln in sys.stdin:
    if ln.startswith('#'):
        continue
    cols = ln.split('\t')
    print cols[0], cols[4]

    c, was_created = Country.objects.get_or_create(
        country_code = cols[0],
        defaults = {'name' : cols[4]}
    )

    c.name = cols[4]
    c.save()


