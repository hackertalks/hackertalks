from tagging.models import Tag
from hackertalks.talks.models import Talk
from hackertalks.stumble.models import StumbleSession

def stumble_tags(request):
    ss = request.session.get('stumble', None)
    if ss:
        ss = StumbleSession.objects.get(id=ss)
    return {'all_tags': sorted(Tag.objects.usage_for_model(Talk, counts=True), key=lambda x: x.count, reverse=True)[:20], 'stumblesession': ss }
