from htseq.centres.models import Centre, CentreCapacity, Platform
from django.template.defaultfilters import slugify
import sys

platforms = [
	Platform.objects.get(short_name='GA2'),
	Platform.objects.get(short_name='454'),
	Platform.objects.get(short_name='SOLiD')
]

for ln in sys.stdin:
	cols = ln.rstrip().split("\t")
	
	c = Centre()
	
	c.name = cols[0]
	c.slug = slugify(cols[0])
	c.notes = cols[1]
	c.url = cols[2]
	
	c.lat, c.long, blah = cols[4].split(",")
	c.service_facility = None
	c.dedicated_genome_centre = None
	
	c.contact_name = ''
	c.contact_email = ''
	c.contact_mask = ''

	c.save()
	
	for n in xrange(5, 8):
		if cols[n].startswith('1'):
			cc = CentreCapacity(
				centre=c,
				platform=platforms[n-5],
				number_machines=None)
			cc.save()
			
			
		
