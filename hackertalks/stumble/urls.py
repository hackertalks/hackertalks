from django.conf.urls.defaults import patterns, include, url
from django.views.generic import detail, list as l
from models import *
from views import *

urlpatterns = patterns('',
    ('^$', l.ListView.as_view(model=Talk, context_object_name='talks'), ),
    ('search/$', search, {}, 'search'),
    ('^(?P<slug>[^/]+)/$', detail.DetailView.as_view(model=Talk, context_object_name='talk'), {}, 'talk',),
    ('stumble/$', detail.DetailView.as_view(model=Talk), {}, 'stumble'),
    ('stumble_on/$', detail.DetailView.as_view(model=Talk), {}, 'stumble_on'),
)
