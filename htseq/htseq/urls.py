from django.conf.urls import patterns, include, url
from django.contrib import admin

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/pending/(?P<id>\d+)/delete/$', 'htseq.centres.views.delete_pending_update', name='delete-pending'),
    url(r'^admin/pending/(?P<id>\d+)/approve/$', 'htseq.centres.views.approve_pending_update', name='approve-pending'),
    (r'^admin/pending/', 'htseq.centres.views.pending_updates'),
    (r'^admin/(.*)', admin.site.urls),
    url(r'^serial', 'htseq.serial.views.serial', name='serial'),
    url(r'^stats', 'htseq.stats.views.stats', name='stats'),
    url(r'^data.json', 'htseq.centres.views.json_list', name='json-data'),
    url(r'^capabilities.json', 'htseq.centres.views.capabilities_json', name='capabilities-json-data'),
    url(r'^platforms/(?P<p_slug>.*)/', 'htseq.centres.views.platform', name='platform'),
    url(r'^centres/(?P<c_slug>.*)/update/$', 'htseq.centres.views.centre_update', name='centre-update'),
    url(r'^centres/(?P<c_slug>.*)/$', 'htseq.centres.views.centre', name='centre'),
    url(r'^update/(?P<id>\d+)/$', 'htseq.centres.views.update_capabilities', name='update-capabilities'),
    url(r'^add/$', 'htseq.centres.views.add_centre', name='add-centre'),
    url(r'^',  'htseq.centres.views.index', name='main')
)
