#!/usr/bin/python

from django.shortcuts import render_to_response

from django.db.models import Avg, Max, Min, Count, Sum
from htseq.centres.models import Centre, CentreCapacity, Country, Platform, Continent
from pygooglechart import PieChart3D

def get_fields(fields, row):
    return [getattr(row, f) for f in fields]

class StatTable:
    def __init__(self, title, queryset, fields, labels=None):
        self.title = title
        self.fields = fields
        self.queryset = queryset
        self.rows = [get_fields(fields, r) for r in queryset]
        if labels:
            self.labels = labels
        else:
            self.labels = fields

def stats(request):
    results = {}

    results['total_machines'] = CentreCapacity.objects.aggregate(Sum('number_machines'))['number_machines__sum']
    results['total_centres'] = Centre.objects.aggregate(Count('id'))['id__count']
    results['machines_per_centre'] = "%.01f" % (float(results['total_machines']) / results['total_centres'])

    results['tables'] = []
    results['tables'].append(StatTable(title='Number of sequencing facilities by country',
        queryset=Country.objects.annotate(num_centres=Count('centre')).order_by('-num_centres').filter(num_centres__gt=0),
        fields=['name', 'num_centres'],
        labels=['Name', 'Number of facilities']))

    results['tables'].append(StatTable(title='Number of sequencing machines by country',
        queryset=Country.objects.annotate(num_machines=Sum('centre__centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
        fields=['name', 'num_machines'],
        labels=['Name', 'Number of machines']))

    results['machines_by_country'] = StatTable(title='Number of sequencing machines by country',
        queryset=Country.objects.annotate(num_machines=Sum('centre__centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
        fields=['country_code', 'name', 'num_machines'],
        labels=['Country Code', 'Country Name', 'Number of Machines'])

    results['tables'].append(StatTable(title='Number of sequencing machines by continent',
        queryset=Continent.objects.annotate(num_machines=Sum('country__centre__centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
        fields=['name', 'num_machines'],
        labels=['Name', 'Number of Machines']))

    results['tables'].append(StatTable(title='Machines by platform',
        queryset=Platform.objects.annotate(num_machines=Sum('centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
        fields=['long_name', 'num_machines'],
        labels=['Name', 'Number of Machines']))

    results['tables'].append(StatTable(title='Centres with platform',
        queryset=Platform.objects.annotate(num_machines=Count('centrecapacity__id')).order_by('-num_machines').filter(num_machines__gt=0),
        fields=['long_name', 'num_machines'],
        labels=['Name', 'Number of centres']))

    # top genome sequencing centres

    results['tables'].append(StatTable(title='Top genome centres',
        queryset=Centre.objects.annotate(num_machines=Sum('centrecapacity__number_machines')).order_by('-num_machines').filter(dedicated_genome_centre=True),
        fields=['name', 'num_machines'],
        labels=['Name', 'Number of Machines']))

    results['tables'].append(StatTable(title='Machines by platform (only genome centres)',
        queryset=Platform.objects.filter(centrecapacity__centre__dedicated_genome_centre=True).annotate(num_machines=Sum('centrecapacity__number_machines')).order_by('-num_machines').filter(num_machines__gt=0),
        fields=['long_name', 'num_machines'],
        labels=['Name', 'Number of Machines']))
    """
    results['tables'].append(StatTable(title='Machines by platform (not genome centres)',
        queryset=Platform.objects.exclude(centrecapacity__centre__dedicated_genome_centre=True).
        annotate(num_machines=Sum('centrecapacity__number_machines')).
        order_by('-num_machines'),
        fields=['long_name', 'num_machines'],
        labels=['Name', 'Number of Machines']))
    """
    return render_to_response('stats.html', results)

    # platforms split by onn-genome sequencing centres




