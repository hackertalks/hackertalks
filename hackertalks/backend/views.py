from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.contrib.auth.models import User
from hackertalks.talks.models import Talk, Conference
from hackertalks.backend.models import UserProfile

@csrf_exempt
def ping(request):
    id = request.POST['id']
    api_key = request.POST['api_key']
    conference_slug = request.POST.get('conference_slug',None)

    conf = None
    try:
        conf = UserProfile.objects.get(api_key=api_key).user.conference_set.all()
        if len(conf)>0:
            conf.filter(slug=conference_slug)
    except UserProfile.DoesNotExist, e:
        print 'nope'
        return HttpResponse('forbidden', status=403)
    except User.DoesNotExist, e:
        conf = None

    blipurl = 'http://blip.tv/rss/%s' % id

    try:
        x = Talk.import_blipurl(blipurl, conf)
        return HttpResponse('imported: %d' % len(x))
    except Exception, e:
        print e
        return HttpResponse('tried to import %s, but %s happened' % (blipurl,e.__repr__()))

