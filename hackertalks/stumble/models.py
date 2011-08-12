import tagging
from datetime import datetime
from hackertalks.talks.models import Talk

from django.db import models

class StumbleSession(models.Model):
    user    = models.ForeignKey(User, null=True)

    params  = models.TextField()        # JSON

class StumbleVisit(models.Model)
    session = models.ForeignKey(StumbleSession)
    talk    = models.ForeignKey(Talk)

