from django.conf import settings

from centres.models import PendingCentreUpdate
from centres.views import do_approve

for updates in PendingCentreUpdate.objects.filter(processed=False).order_by('date_created'):
	print "Doing %s" % (updates,)
	do_approve(updates.pk)
 
