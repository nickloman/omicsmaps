from akismet import Akismet

api = Akismet(agent='omicsmaps/1.0')
print api.verify_key()

import settings

from centres.models import PendingCentreUpdate
from centres.views import do_approve

"""
   name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, db_index=True)
    url = models.URLField(max_length=255, help_text='The official website for this sequencing facility')
    notes = models.TextField(blank=True)
    lat = models.FloatField(help_text='Drag the map marker to change the position of this facility')
    long = models.FloatField()
    service_facility = models.NullBooleanField(help_text='Does this facility offer a sequencing service to the public?')
    dedicated_genome_centre = models.NullBooleanField(help_text='Is this facility a dedicated genome-sequencing centre?')
    contact_name = models.CharField(null=True, blank=True, max_length=100, help_text='The contact name for enquiries to this sequencing centre')
    contact_email = models.CharField(null=True, blank=True, max_length=100)
    contact_mask = models.CharField(null=True, blank=True, max_length=100)
    locality = models.CharField(max_length=100)
    country = models.ForeignKey(Country, null=True)
    capacity_summary = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)"""

for updates in PendingCentreUpdate.objects.filter(processed=False).order_by('date_created'):
	text = """
%s
%s
%s
%s
%s
%s""" % (updates.name, updates.url, updates.notes, updates.contact_email, updates.contact_name, updates.slug)
	print text
	text = updates.notes
	print " --- "
	try:
		if not api.comment_check(text, {'user_ip':'127.0.0.1', 'user_agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'}):
        		do_approve(updates.pk)
		else:
			print "RUBBISH"
	except Exception, e:
		pass
