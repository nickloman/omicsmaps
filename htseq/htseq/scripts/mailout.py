#!/usr/bin/python

from htseq.centres.models import Centre
from django.core.mail import send_mail


import re

TEXT = """
Hi there

I am one of the curators of the world high-throughput sequencing
map, located at http://pathogenomics.bham.ac.uk/hts/

Thanks to the efforts of the community we now track almost 400
sequencing centres and 1,144 machines on the map - we estimate
that is between half and two-thirds of all machines in the world.

The map has proven very popular and we have recently updated it to
account for the new sequencers on the market (HiSeq, PacBio and
SOLiD4).

We have also made it easier for visitors to find sequencing service
providers via the map, which will hopefully result in more
enquiries and collaborations being made.

We're keen to ensure that the map is as current and useful as
possible.

The information about your centre visible to the public is:
http://pathogenomics.bham.ac.uk/hts/centres/%s/

We'd be very grateful if you could take a moment to update your
details by visiting the following link and ensuring each item
is correct. Note there are two pages of information to fill out,
please check that the type and number of sequencers in your
centre is correect.

http://pathogenomics.bham.ac.uk/hts/centres/%s/update/

If for some reason this email has gone to the wrong person, I'd
be grateful if you could forward this message. 

Note that changes to the map are moderated and so do not appear
immediately, give it a few hours.

If you have any comments, questions or suggestions on the map
I'd love to here from you.

Best regards

Nick

PS If you don't want to be contacted in the future, please update
your centre profile accordingly to remove or change your email 
address.
"""

def go():
    start = False
    for c in Centre.objects.all():
        if c.contact_email:
            # print c.name.encode('ascii', 'ignore'), c.contact_name.encode('ascii', 'ignore'), c.contact_email.encode('ascii', 'ignore')

            emails = re.split("[,\;]+", c.contact_email.encode('ascii', 'ignore'))
            emails = [e.strip() for e in emails]

            if 'chen0010ibms.sinica.edu.tw' in emails:
                start = True

            if start:
                print "mailing" + str(emails)
                send_mail('World sequencing map of high-throughput sequencers', TEXT % (c.slug, c.slug),
                       'Nick Loman <n.j.loman@bham.ac.uk>', emails, fail_silently=True)
            else:
                print "skipping" + str(emails)

go()
