import tagging
from datetime import datetime
from hackertalks.talks.models import Talk
from django.db import models
from django.contrib.auth.models import User
import json

class StumbleSession(models.Model):
    user    = models.ForeignKey(User, null=True)

    params  = models.TextField()        # JSON

    @property
    def parsedparams(self):
        if not hasattr(self, 'param_cache'):
            self.param_cache = json.loads(self.params)

        return self.param_cache


    def get_next(self):
        params = self.parsedparams
        f = Talk.objects.filter(duration__gte=params['duration_lower'],
                                duration__lte=params['duration_upper']
                                )
        f = f.exclude(id__in=[x.talk_id for x in self.stumblevisit_set.all()])

        for talk in f:
            if not params['tags']:
                return talk
            for tag in params['tags']:
                for talktag in talk.tags:
                    if tag == talktag.name:
                        return talk
        return None


class StumbleVisit(models.Model):
    session = models.ForeignKey(StumbleSession)
    talk    = models.ForeignKey(Talk)

