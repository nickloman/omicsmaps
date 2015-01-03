from django.forms import ModelForm
from models import SerialNumber

class SerialForm(ModelForm):
    class Meta:
        model = SerialNumber 
        exclude = ['ip_address', 'added_at', 'approved']


