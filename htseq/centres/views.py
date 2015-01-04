from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext

from forms import CentreForm
from geolocate import geolocate
import json
from django.conf import settings
import pygeoip

from models import Centre, CentreCapacity, Platform, Country, copy_model_instance, PendingCentreUpdate, PendingCentreCapacity, get_fields

def hash_by_attribute(queryset, attribute):
    hash = {}
    for rec in queryset:
        val = getattr(rec, attribute)
        if val in hash:
            hash[val].append(rec)
        else:
            hash[val] = [rec]
    return hash, sorted(hash.keys())

def lookup_country(request):
    gi = pygeoip.GeoIP(settings.GEOIP_DATA)
    country_code = gi.country_code_by_addr(request.META.get('REMOTE_ADDR') )
    if not country_code:
        return 'GB'
    return country_code

def standard_items(request):
    centres = Centre.objects.select_related('country').order_by('country__name', 'name')
    return {'google_api_key' : settings.GOOGLE_API_KEY,
            'centres' : centres,
            'static_path' : settings.STATIC_PATH,
            'centre_mode' : False,
            'static_version' : settings.STATIC_VERSION,
            'platforms' : Platform.objects.order_by('short_name'),
            'country' : lookup_country(request)
    }

def index(request):
    params = standard_items(request)
    params['recent'] = Centre.objects.all().order_by('-id')[0:4]
    return render_to_response('index.html', params)

def make_capability_matrix(request):
    {'centres' : [platform]}

def country_to_dict(c):
    return {'name' : str(c.name), 'sw_lat' : str(c.sw_lat), 'sw_long' : str(c.sw_long), 'ne_lat' : str(c.ne_lat), 'ne_long' : str(c.ne_long)}

def objects_to_dict(objects, fields, attrs):
    r = []
    for o in objects:
        d = dict([(k, unicode(v)) for k, v in get_fields(o).iteritems() if k in fields])
        d.update(dict([(a, getattr(o, a)) for a in attrs]))
        r.append(d)
    return r

def get_centres_with_count(service_provider=False):
    from django.db import models
    centrecapacitylist = CentreCapacity.objects.select_related('centre', 'centre__country')
    if service_provider:
        centrecapacitylist = centrecapacitylist.filter(centre__service_facility=True)
    centres = {}
    for capacity in centrecapacitylist:
        if capacity.centre.pk in centres:
            centre = centres[capacity.centre.pk]
        else:
            centre = capacity.centre
            centres[centre.pk] = centre
        n = getattr(centre, 'n', 0)
        if capacity.number_machines:
            n += capacity.number_machines
        else:
            n += 1
        setattr(centre, 'n', n)
    centres = centres.values()
    import operator
    centres.sort(key=operator.attrgetter('case_insensitive_name'))
    return centres

from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def json_list(request):
    response = HttpResponse(content_type='application/json')

    json_object = {}
    # centres = Centre.objects.select_related('country')
    centres = get_centres_with_count()
    json_object['centres'] = objects_to_dict(centres, fields=('name', 'slug', 'lat', 'long', 'capacity_summary'), attrs=('n', 'loc',))

    # json_object['platform'] = objects_to_dict(Platform.objects.all(), fields=('short_name',))
    # json_object['capabilities'] = objects_to_dict(CentreCapacity.objects.all(), fields=('centre', 'platform'))

    countries = {}
    for centre in centres:
        countries[str(centre.country.name)] = country_to_dict(centre.country)
    json_object['countries'] = countries

    json.dump(json_object, response, ensure_ascii=False)
    return response

def capabilities_json(request):
    response = HttpResponse(content_type='application/json')
    id_list = request.GET['platform'].strip().split(',')
    id_list = [id for id in id_list if id != '']

    service_provider = False
    if 'service' in id_list:
        service_provider = True
        id_list.remove('service')

    mode = request.GET.get('mode', 'OR')
    if len(id_list):
        capabilities = CentreCapacity.objects.select_related('centre').filter(platform__in=id_list)
        if service_provider:
            capabilities = capabilities.filter(centre__service_facility=True)
        centre_counts = {}
        if mode == 'AND':
            centres = {}
            for c in capabilities:
                if c.centre.pk in centres:
                    centre = centres[c.centre.pk]
                else:
                    centre = c.centre
                    centres[centre.pk] = centre

                if c.centre in centre_counts:
                    centre_counts[c.centre] += 1
                else:
                    centre_counts[c.centre] = 1

                n = getattr(centre, 'n', 0)
                if c.number_machines:
                    n += c.number_machines
                else:
                    n += 1
                setattr(centre, 'n', n)

            centres = [centres[c.pk] for c, count in centre_counts.iteritems() if count == len(id_list)]
        elif mode == 'OR':
            centres = [c.centre for c in capabilities]
    else:
        centres = get_centres_with_count(service_provider)
    capabilities = objects_to_dict(centres, fields=('name', 'slug', 'lat', 'long', 'capacity_summary'), attrs=('n', 'loc',))
    json.dump(capabilities, response, ensure_ascii=False)
    return response

def centre(request, c_slug):
    params = standard_items(request)
    params['c'] = get_object_or_404(Centre, slug=c_slug)
    params['capacity'] = CentreCapacity.objects.filter(centre=params['c']).order_by('centre__name')
    params['centre_mode'] = True
    return render_to_response('centre.html', params)

def platform(request, p_slug):
    platform = Platform.objects.get(slug=p_slug)
    centres = CentreCapacity.objects.filter(platform=platform).select_related('centre').order_by('centre__name')
    centres = [c.centre for c in centres]
    return render_to_response('platform.html', {'p' : platform, 'centres' : centres})

def update_form(c):
    params = {}
    params['form'] = CentreForm(instance=c)
    #CapacityFormSet = inlineformset_factory(Centre, CentreCapacity)
    #params['formset'] = CapacityFormSet(instance=c)
    return params

def centre_update(request, c_slug):
    params = standard_items(request)
    c = get_object_or_404(Centre, slug=c_slug)
    pcu = copy_model_instance(c, PendingCentreUpdate)

    if request.POST:
        f = CentreForm(request.POST, instance=pcu)
        if f.is_valid():
            pcu = f.save(commit=False)
            pcu.update_to = c
            pcu.processed = False
            pcu.ip_address = request.META.get('REMOTE_ADDR', 'n/a')
            pcu.email_address = 'n.j.loman@bham.ac.uk'

            pcu.save()
            return HttpResponseRedirect(reverse('update-capabilities', args=[pcu.id]))
    else:
        f = CentreForm(instance=pcu)
    params['form'] = f
    return render_to_response('update.html', params, context_instance=RequestContext(request))

def add_centre(request):
    params = standard_items(request)

    if request.POST:
        f = CentreForm(request.POST)
        if f.is_valid():
            pcu = f.save(commit=False)
            pcu.processed = False
            pcu.ip_address = request.META.get('REMOTE_ADDR', 'n/a')
            pcu.email_address = 'n.j.loman@bham.ac.uk'
            pcu.save()

            return HttpResponseRedirect(reverse('update-capabilities', args=[pcu.id]))
    else:
        c = PendingCentreUpdate()
        c.lat = request.GET.get('lat')
        c.long = request.GET.get('long')
        try:
            country_name, country_code, c.locality = geolocate(c.lat, c.long)
            c.country = Country.objects.get(country_code = country_code)
        except ValueError:
            pass

        f = CentreForm(instance=c)
    params['form'] = f
    return render_to_response('update.html', params, context_instance=RequestContext(request))

def update_capabilities(request, id):
    pcu = get_object_or_404(PendingCentreUpdate, pk=id)
    params = standard_items(request)

    PendingCentreCapacity.objects.filter(centre = pcu).delete()
    if pcu.update_to:
        for cc in CentreCapacity.objects.filter(centre = pcu.update_to):
            PendingCentreCapacity(centre = pcu, platform=cc.platform, number_machines=cc.number_machines).save()

    CapacityFormSet = inlineformset_factory(PendingCentreUpdate, PendingCentreCapacity)
    if request.POST:
        formset = CapacityFormSet(request.POST, instance=pcu)
        if formset.is_valid():
            formset.save()
        else:
            print formset.errors

        from django.core.mail import mail_admins
        mail_admins('Sequencing map updated', 'Visit http://pathogenomics.bham.ac.uk/hts/admin/pending/', fail_silently=True)
        return HttpResponse('Thanks for your update. It will be reviewed by our moderators. Back to the <a href="' + reverse('main') + '">home</a> page.')
    else:
        formset = CapacityFormSet(instance=pcu)
    params['form'] = formset
    params['caps_mode'] = True
          
    return render_to_response('update.html', params, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff, login_url='/hts/admin/')
def pending_updates(request):
    updates = PendingCentreUpdate.objects.filter(processed=False).order_by('date_created')
    return render_to_response('pending-updates.html', {'updates' : updates})

def do_approve(id):
    u = get_object_or_404(PendingCentreUpdate, pk=id)
    if u.update_to:
        c = u.update_to
    else:
        c = Centre()
    c.merge(u)
    c.save()

    CentreCapacity.objects.filter(centre = c).delete()
    for cc in PendingCentreCapacity.objects.filter(centre = u):
        CentreCapacity(centre = c, platform=cc.platform, number_machines=cc.number_machines).save()

    u.processed = True
    u.save()
    # update capacity summary 
    c.save()
    return HttpResponseRedirect(reverse('htseq.centres.views.pending_updates'))

@user_passes_test(lambda u: u.is_staff, login_url='/hts/admin/')
def approve_pending_update(request, id):
    do_approve(id)
    return HttpResponseRedirect(reverse('htseq.centres.views.pending_updates'))

@user_passes_test(lambda u: u.is_staff, login_url='/hts/admin/')
def delete_pending_update(request, id):
    u = get_object_or_404(PendingCentreUpdate, pk=id)
    u.delete()
    return HttpResponseRedirect(reverse('htseq.centres.views.pending_updates'))

