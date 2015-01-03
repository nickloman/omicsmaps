#!/usr/bin/python

from django.db.models import Avg, Max, Min, Count, Sum
from htseq.centres.models import Centre, CentreCapacity, Country, Platform, Continent

from pygooglechart import PieChart3D

total_machines = CentreCapacity.objects.aggregate(Sum('number_machines'))['number_machines__sum']
total_centres = Centre.objects.aggregate(Count('id'))['id__count']

print "Total number of machines: %d" % (total_machines,)
print "Total number of centres: %d" % (total_centres,)
print "Machines per centre: %d" % (total_machines / total_centres,)

# sites by country

def stat(title, queryset, fields):
    print title
    print "-" * 60
    for r in queryset:
        print "\t".join([unicode(getattr(r, f)).encode('ascii', 'ignore') for f in fields])
    print

stat(title='Number of sequencing facilities by country',
     queryset=Country.objects.annotate(num_centres=Count('centre')).order_by('-num_centres').filter(num_centres__gt=0),
     fields=['name', 'num_centres'])

stat(title='Number of sequencing machines by country',
     queryset=Country.objects.annotate(num_machines=Sum('centre__centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
     fields=['name', 'num_machines'])

stat(title='Number of sequencing machines by continent',
     queryset=Continent.objects.annotate(num_machines=Sum('country__centre__centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
     fields=['name', 'num_machines'])

stat(title='Machines by platform',
     queryset=Platform.objects.annotate(num_machines=Sum('centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
     fields=['long_name', 'num_machines'])

stat(title='Centres with platform',
     queryset=Platform.objects.annotate(num_machines=Count('centrecapacity__id')).order_by('-num_machines').filter(num_machines__gt=0),
     fields=['long_name', 'num_machines'])

# top genome sequencing centres

stat(title='Top genome centres',
    queryset=Centre.objects.annotate(num_machines=Sum('centrecapacity__number_machines')).order_by('-num_machines').filter(dedicated_genome_centre=True),
    fields=['name', 'num_machines'])

stat(title='Machines by platform (only genome centres)',
     queryset=Platform.objects.filter(centrecapacity__centre__dedicated_genome_centre=True).annotate(num_machines=Sum('centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
     fields=['long_name', 'num_machines'])

stat(title='Machines by platform (not genome centres)',
     queryset=Platform.objects.
        annotate(num_machines=Sum('centrecapacity__number_machines')).
        order_by('-num_machines'),
     fields=['long_name', 'num_machines'])


# platforms split by onn-genome sequencing centres







