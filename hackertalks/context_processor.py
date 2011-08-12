from tagging.models import Tag

def stumble_tags(request):
    return {'all_tags': Tag.objects.all() }
