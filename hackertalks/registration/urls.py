from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as authviews

urlpatterns = patterns('',
    url(r'^login/$', authviews.login, {}, 'auth_login'),
    url(r'^logout/$', authviews.logout, {}, 'auth_logout'),
    url(r'^register/$', 'hackertalks.registration.views.register',),
)
