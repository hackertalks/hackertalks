import copy,re
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Talk


def search(request):
    search_term = request.GET['term']

    search_terms = re.findall(r'\w{3,}', search_term)

    print search_terms
    results = {}

    weights = [(10, lambda x: Q(title__icontains=x),),
               ( 5, lambda x: Q(description__icontains=x),),
               ( 1, lambda x: Q(speakers__name__icontains=x),),
              ]

    for term in search_terms:
        for weight, fun in weights:
            for x in Talk.objects.filter(fun(term)):
                results.setdefault(x.slug, [0, x,])
                results[x.slug][0]+=weight

    v = copy.copy(results.values())
    v.sort(lambda x,y: x[0]<y[0])

    r = [x[1] for x in v]

    return render_to_response('talks/talk_list.html', {'talks': r, 'terms': search_terms, 'search': True}, context_instance=RequestContext(request))
