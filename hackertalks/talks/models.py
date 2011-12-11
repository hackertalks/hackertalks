import tagging
import feedparser
import re
from django.db import models
from django.db.models import signals
from autoslug import AutoSlugField
from datetime import datetime
from html2text import html2text

from django.contrib.auth.models import User
from datetime import datetime, timedelta
import json
from tagging.models import Tag

class License(models.Model):
    name            = models.TextField()
    shortname       = models.TextField()
    abbreviation    = models.CharField(max_length=100,unique=True)
    link            = models.TextField()
    thumbnail       = models.TextField()
    description     = models.TextField()
    shareable       = models.BooleanField()


    def __unicode__(self):
        return self.abbreviation

class Speaker(models.Model):
    name            = models.TextField()
    slug            = AutoSlugField(max_length=100, populate_from='name', unique=True)
    title           = models.TextField()
    
    def __unicode__(self):
        return self.name

class Conference(models.Model):
    name            = models.TextField()
    slug            = AutoSlugField(max_length=100, populate_from='name', unique=True)
    url             = models.CharField(max_length=50, null=True)

    admin           = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.name

class Talk(models.Model):
    title           = models.CharField(max_length=100, null=False, blank=False)
    license         = models.ForeignKey(License, null=True, to_field='abbreviation')
    slug            = AutoSlugField(max_length=100, populate_from='title', unique=True)
    description     = models.TextField()
    conference      = models.ForeignKey(Conference, null=True)

    duration        = models.IntegerField(null=True)

    video_embedcode = models.TextField()
    video_bliptv_id = models.TextField()
    video_image     = models.TextField()

    speakers        = models.ManyToManyField(Speaker)

    def refresh_from_blip(self):
        Talk.import_blipurl(Talk.rss_url_for(self.video_bliptv_id), self.conference)

    @classmethod
    def rss_url_for(cls, id):
        return 'http://blip.tv/rss/%s' % id
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('talk', (), {'slug': self.slug},)

    @classmethod
    def import_blipurl(cls, feedurl, conference):
        imported = []
        x = feedparser.parse(feedurl)

        for item in x['entries']:
            print item
            ts = []
            try:
                ts = Talk.objects.filter(video_bliptv_id=item['blip_posts_id'].strip())
            except:
                print """if you see this, either blip has changed their API (unlikely) or you don't have python-libxml2 installed which makes 
                         feedparser behave awkwardly. """
                raise
            t = ts[0] if len(ts) else Talk()

            t.title=item['title'].strip()
            t.description=html2text(item['description']).replace(t.title, '')

            #t.conference=conference
            image = item.get('media_thumbnail', item.get('blip_picture', None))
            try:
                image = image[0]['url']
            except Exception, e:
                print image, e
            t.video_image=item.get('blip_smallthumbnail', image)
            t.video_bliptv_id=item['blip_posts_id'].strip()
            t.video_embedcode=item['media_player']['content'].replace('embed', 'embed wmode="transparent"')
            if item['blip_runtime'].strip():
                t.duration=item['blip_runtime'] and int(item['blip_runtime'])/60 # minutes
            t.license=License.objects.filter(name=item['blip_license'])[0]


            t = cls.import_blipurl_parseout(t)

            t.save()
            [Tag.objects.add_tag(t, x['term'].replace(' ','-')) for x in item['tags']]
            imported.append(t)
        return imported

    @classmethod
    def import_blipurl_parseout(cls, t):
        """ try to magically parse conference and speaker names """

        """ conference:title """
        """ OSCON 09: Clay Johnson, "Apps for America" """
        conference = None
        x = re.match(r'^([^:]+):(.*)$', t.title)
        if x:
            conference=x.groups()[0].strip()
            t.title=x.groups()[1].strip()

        """ speakers, "title" """
        x = re.match(r'^([^"]+)"([^"]+)"$', t.title)
        if x:
            name_match = x.groups()[0].strip().split(',')
            name = name_match[0].strip()
            job_title = name_match[1].strip() if len(name_match)>1 else ''
            t.save()
            for namestr in name.split(' and '):
                ss, created = Speaker.objects.get_or_create(name=namestr, title=job_title)
                t.speakers.add(ss)
            t.title=x.groups()[1]
        if conference:
            t.title+=' (%s)' % conference
        return t

class TalkFeature(models.Model):
    talk            = models.ForeignKey(Talk)
    date            = models.DateField(default=datetime.today)

    def __unicode__(self):
        return u'%s on %s' % (self.date, self.talk.title,)


tagging.register(Talk)
