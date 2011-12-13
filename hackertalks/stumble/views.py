from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import StumbleSession, StumbleVisit

import json

def stumble_next(request):
    sid = request.session.get('stumble', None)
    if not sid:
        return render_to_response('stumble/done.html', context_instance=RequestContext(request))
    ss = StumbleSession.objects.get(pk=sid)
    t = ss.get_next()
    if t:
        StumbleVisit.objects.create(session=ss, talk=t)
        return redirect(t)
    return render_to_response('stumble/done.html', context_instance=RequestContext(request))

def stumble(request):
    user = request.user if request.user.is_authenticated() else None
    params = {
        'tags': request.POST.getlist('tags'),
        'duration_lower': int(request.POST.get('duration_start',10)),
        'duration_upper': int(request.POST.get('duration_end', 90)),
    }

    print request.POST

    ss = StumbleSession.objects.create(params = json.dumps(params),
                                       user = user)
    request.session['stumble'] = ss.id
    return redirect('stumble_next')

