from django.conf.urls.defaults import patterns, include, url
from models import Talk
from django.views.generic import detail, list as l
from views import search

urlpatterns = patterns('',
    ('^$', l.ListView.as_view(model=Talk, context_object_name='talks'), ),
    ('search/$', search, {}, 'search'),
    ('^(?P<slug>[^/]+)/$', detail.DetailView.as_view(model=Talk, context_object_name='talk'), {}, 'talk',),
)
