from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^ping/$', views.ping, {}, 'backend_ping_url'),
)
