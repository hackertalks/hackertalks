import feedparser
from datetime import *
from paste.script.command import Command

import hackertalks.model
from hackertalks.model import meta

class Import_BlipUser(Command):
    summary = "--NO SUMMARY--"
    usage = "--NO USAGE--"
    group_name = "hackertalks"
    parser = Command.standard_parser(verbose=False)

    def command(self):
        x = feedparser.parse('http://%s.blip.tv/rss' % self.args[0])

        for item in x['entries']:
#            print item['blip_embedurl']
            if int(item['blip_runtime'])==0:
                print item['link']
#            print timedelta(seconds=int(item['blip_runtime']))

