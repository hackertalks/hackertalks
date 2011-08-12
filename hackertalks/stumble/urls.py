from django.conf.urls.defaults import patterns, include, url
from django.views.generic import detail, list as l
from models import *
from views import *

urlpatterns = patterns('',
    ('stumble/$', stumble, {}, 'stumble'),
    ('stumble_next/$', stumble_next, {}, 'stumble_next'),
)
