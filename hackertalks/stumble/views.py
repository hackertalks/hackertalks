from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from models import StumbleSession, StumbleVisit

import json

def stumble_next(request):
    sid = request.session.get('stumble', None)
    if not sid:
        return
    ss = StumbleSession.objects.get(pk=sid)
    t = ss.get_next()
    StumbleVisit.objects.create(session=ss, talk=t)
    return redirect(t)

def stumble(request):
    user = request.user if request.user.is_authenticated else None
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

