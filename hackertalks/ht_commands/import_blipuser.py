from datetime import *
from paste.script.command import Command

import hackertalks.model as model
from hackertalks.model import meta
import re

from hackertalks.config.environment import load_environment
from paste.deploy import appconfig
from html2text import html2text

class Import_BlipUser(Command):
    summary = "import $username.blip.tv"
    usage = "import_blipuser $username --config $configfile"
    group_name = "hackertalks"
    parser = Command.standard_parser(verbose=False)

    parser.add_option('-c', '--config', dest="config", default="development.ini", help='config')

    def command(self):
        conf = appconfig('config:%s' % self.options.config, relative_to='.')
        load_environment(conf.global_conf, conf.local_conf)
        
        Talk.import_blipurl('http://%s.blip.tv/rss' % self.args[0])
