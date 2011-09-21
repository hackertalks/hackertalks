import views

urlpatterns = patterns('',
    url(r'^ping$', views.ping, {}, 'backend_ping_url'),
)
