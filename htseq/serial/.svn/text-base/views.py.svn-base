# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse
from forms import SerialForm
from models import SerialNumber

def serial(request):
    n = SerialNumber.objects.count()
    if request.POST:
        form = SerialForm(request.POST)
        if form.is_valid():
            serial_number = form.save(commit = False)
            serial_number.ip_address = request.META.get('REMOTE_ADDR', 'n/a')
            serial_number.save()
            return HttpResponse('Thanks very much for submitting this data. Check back soon for the results!')
    else:
        form = SerialForm()
    return render_to_response('serial.html', {'form' : form, 'n' : n})

