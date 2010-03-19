import feedparser
from datetime import *
from paste.script.command import Command

import hackertalks.model as model
from hackertalks.model import meta
import re

from hackertalks.config.environment import load_environment
from paste.deploy import appconfig

class Import_BlipUser(Command):
    summary = "--NO SUMMARY--"
    usage = "--NO USAGE--"
    group_name = "hackertalks"
    parser = Command.standard_parser(verbose=False)

    parser.add_option('-c', '--config', dest="config", default="development.ini", help='config')

    def command(self):
        conf = appconfig('config:%s' % self.options.config, relative_to='.')
        load_environment(conf.global_conf, conf.local_conf)
        
        x = feedparser.parse('http://%s.blip.tv/rss' % self.args[0])

        for item in x['entries']:
            ts = []
            try:
                ts = meta.Session.query(model.Talk).filter(model.Talk.video_bliptv_id==int(item['blip_item_id'])).all()
            except:
                print """if you see this, either blip has changed their API (unlikely) or you don't have python-libxml2 installed which makes 
                         feedparser behave awkwardly. """
                return -1
            t = ts[0] if len(ts) else model.Talk()

            t.title=item['title']
            t.description=item['description']
            t.conference=self.args[0]
            t.thumbnail_url=item['blip_smallthumbnail']
            t.video_bliptv_id=item['blip_item_id']
            t.short_title=''
            t.video_embedcode=item['media_player'].replace('embed', 'embed wmode="transparent"')
            t.video_duration=timedelta(seconds=int(item['blip_runtime']))
            t.license=meta.Session.query(model.License).filter(model.License.name==item['blip_license']).one()


            t.tags=list(set([model.Tag.get_or_create(y['term'].lower()) for y in item['tags']]))


            """ try to magically parse conference and speaker names """

            """ OSCON 09: Clay Johnson, "Apps for America" """
            x = re.match('^([^:]+):([^"]+)"([^"]+)"$', t.title)
            print t.title, x
            if x:
                name_match = x.groups()[1].strip().split(',')
                name = name_match[0].strip()
                job_title = name_match[1].strip() if len(name_match)>1 else ''

                t.speakers=[]
                for namestr in name.split(' and '):
                    ss = meta.Session.query(model.Speaker).filter(model.Speaker.name==namestr).filter(model.Speaker.job_title==job_title).all()
                    s = ss[0] if ss else model.Speaker(name=namestr, job_title=job_title)
                    meta.Session.merge(s)
                    t.speakers.append(s)
                t.title=x.groups()[2]


            meta.Session.merge(t)
            meta.Session.commit()

