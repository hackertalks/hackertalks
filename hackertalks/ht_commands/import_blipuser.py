import feedparser
from datetime import *
from paste.script.command import Command

import hackertalks.model as model
from hackertalks.model import meta

from hackertalks.config.environment import load_environment
from paste.deploy import appconfig
conf = appconfig('config:development.ini', relative_to='..')
load_environment(conf.global_conf, conf.local_conf)

class Import_BlipUser(Command):
    summary = "--NO SUMMARY--"
    usage = "--NO USAGE--"
    group_name = "hackertalks"
    parser = Command.standard_parser(verbose=False)

    def command(self):
        meta.Session.commit()
        x = feedparser.parse('http://%s.blip.tv/rss' % self.args[0])

        for item in x['entries']:
            ts = meta.Session.query(model.Talk).filter(model.Talk.video_bliptv_id==int(item['blip_item_id'])).all()
            t = ts[0] if len(ts) else model.Talk()

            t.title=item['title']
            t.description=item['description']
            t.conference=self.args[0]
            t.thumbnail_url=item['blip_smallthumbnail']
            t.video_bliptv_id=item['blip_item_id']
            t.short_title=''
            t.video_embedcode=item['media_player']
            t.video_duration=timedelta(seconds=int(item['blip_runtime']))

            meta.Session.add(t)
            meta.Session.commit()

