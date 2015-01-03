from django.db import models
from htseq.centres.models import Platform
from django.contrib import admin

# Create your models here.

class SerialNumber(models.Model):
    serial_number = models.CharField(max_length=40)
    platform = models.ForeignKey(Platform)
    installation_date = models.CharField(max_length=40, verbose_name="Approximate installation date i.e. month and year")
    location = models.CharField(max_length=60)
    approved = models.BooleanField()
    ip_address = models.IPAddressField()
    added_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s" % (self.platform, self.serial_number)

admin.site.register(SerialNumber)
