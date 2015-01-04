from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.db.models import AutoField
from django.core.exceptions import ObjectDoesNotExist

def get_fields(obj):
    fields = dict([(f.name, getattr(obj, f.name))
                   for f in obj._meta.fields
                   if not isinstance(f, AutoField) and\
                       not f in obj._meta.parents.values()])
    return fields

def copy_model_instance(obj, newobj):
    initial = get_fields(obj)
    return newobj(**initial)

class Location(models.Model):
    name = models.TextField(max_length=100)
    
    sw_lat = models.FloatField(null=True)
    sw_long = models.FloatField(null=True)
    ne_lat = models.FloatField(null=True)
    ne_long = models.FloatField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class Continent(Location):
    pass
        
class Country(Location):
    country_code = models.TextField(max_length=2)
    continent = models.ForeignKey(Continent, null=True)

class CentreBase(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, db_index=True, unique=True)
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
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __unicode__(self):
        return self.name

    @property
    def email_bits(self):
        return self.contact_email.split("@")

    @property
    def case_insensitive_name(self):
        return self.name.lower()

    @property
    def loc(self):
        return "%s, %s" % (self.locality, self.country)

    def save(self):
        self.slug = slugify(self.name)
        super(CentreBase, self).save()

    class Meta:
        abstract = True

class Centre(CentreBase):
    def save(self):
        self.capacity_summary = ''
        cs = ''
        for cc in self.centrecapacity_set.all():
            try:
               if cc.number_machines:
                  cs += " %d x " % (cc.number_machines)
               cs += cc.platform.short_name
               cs += ','
            except ObjectDoesNotExist, e: 
               print "Skipping as platform not exist"
        self.capacity_summary = cs.rstrip(',')
        super(Centre, self).save()

    def merge(self, obj):
        fields = get_fields(self)
        for f in fields.keys():
            setattr(self, f, getattr(obj, f))

    class Meta:
        db_table = 'centre'

class ComparisonLine:
    def __init__(self, field, x, y):
        self.old = x
        self.new = y
        if self.old == self.new:
            self.changed = False
        else:
            self.changed = True
        self.field = field

class PendingCentreUpdate(CentreBase):
    ip_address = models.CharField(max_length=16)
    email_address = models.CharField(max_length=200)
    update_to = models.ForeignKey(Centre, null=True)
    processed = models.BooleanField()

    @property
    def update_type(self):
        if self.update_to:
            return 'update'
        else:
            return 'new'

    @property
    def compare(self):
        c = self.update_to
        if not c:
            c = Centre()
        lines = []
        for f in get_fields(c):
            lines.append(ComparisonLine(f, getattr(c, f), getattr(self, f)))
        return lines
    
class Platform(models.Model):
    short_name = models.TextField()
    long_name = models.TextField()
    slug = models.TextField(db_index=True)    
    manufacturer_website = models.TextField()

    def __unicode__(self):
        return self.short_name
    
    class Meta:
        db_table = 'platform'
    
class CentreCapacityBase(models.Model):
    platform = models.ForeignKey(Platform)
    number_machines = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return "%s - %s" % (str(self.centre), str(self.platform))
    
    class Meta:
        abstract = True
        
class CentreCapacity(CentreCapacityBase):
    centre = models.ForeignKey(Centre)

    class Meta:
        db_table = 'centre_capacity'

class PendingCentreCapacity(CentreCapacityBase):
    centre = models.ForeignKey(PendingCentreUpdate)

class CapacityInline(admin.TabularInline):
    model = CentreCapacity

class CentreAdmin(admin.ModelAdmin):
    inlines = [
        CapacityInline,
    ]

class PendingCapacityInline(admin.TabularInline):
    model = PendingCentreCapacity

class PendingCentreAdmin(admin.ModelAdmin):
    inlines = [
        PendingCapacityInline,
    ]

#admin.site.register(Centre, CentreAdmin)
# admin.site.register(Platform)
#admin.site.register(CentreCapacity)
#admin.site.register(Country)
#admin.site.register(Continent)
#admin.site.register(PendingCentreUpdate, PendingCentreAdmin)

