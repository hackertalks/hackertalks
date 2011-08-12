from tagging.models import Tag
from hackertalks.talks.models import Talk

def stumble_tags(request):
    return {'all_tags': sorted(Tag.objects.usage_for_model(Talk, counts=True), key=lambda x: x.count, reverse=True)[:20] }
