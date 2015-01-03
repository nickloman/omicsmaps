from django.forms import ModelForm
from models import PendingCentreUpdate

class CentreForm(ModelForm):
    class Meta:
        model = PendingCentreUpdate
        exclude = ('slug', 'contact_mask', 'date_created', 'ip_address', 'email_address', 'update_to', 'processed', 'capacity_summary')
