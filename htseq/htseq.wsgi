import os
import sys

# redirect stdout
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'htseq.settings'

sys.path.append('/home/nick/maps/htseq')
sys.path.append('/home/nick/maps')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

