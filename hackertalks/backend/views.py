from hackertalks.talks.models import Talk, Conference
from django.core.http import *

def ping(request):
    id = request.POST['id']
    api_key = request.POST['api_key']
    conference_slug = request.POST.get('conference_slug',None)

    conf = None
    try:
        conf = UserProfile.get(api_key=api_key).user.conference_set.all()
        if conf.length>0:
            conf.filter(slug=conference_slug)
    except UserProfile.NotFound, e:
        print 'nope'
        return HttpForbidden()

    blipurl = 'http://blip.tv/file/%s/?skin=rss' % id

    try:
        x = Talk.import_blipurl(blipurl, conf)
        return HttpResponse('imported: %d' % len(x))
    except Exception, e:
        return HttpResponse('tried to import %s, but %s happened' % (blipurl,e))

