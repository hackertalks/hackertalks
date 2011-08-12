from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.list import ListView
from hackertalks.talks.models import TalkFeature
from datetime import date, timedelta

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackertalks.views.home', name='home'),
    # url(r'^hackertalks/', include('hackertalks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^talks/', include('hackertalks.talks.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^$', ListView.as_view(queryset=TalkFeature.objects.filter(date__lte=date.today()).order_by('-date'), context_object_name='featured_talks'),),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
