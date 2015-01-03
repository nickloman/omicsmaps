#!/usr/bin/python
from htseq.centres.models import Centre

for c in Centre.objects.all():
    c.save()

