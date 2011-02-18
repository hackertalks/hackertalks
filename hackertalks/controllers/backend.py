import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort

from hackertalks.lib.base import BaseController, render

from hackertalks.model import Uploader, Talk
from hackertalks.model.meta import Session
from datetime import datetime
from hackertalks.controllers.halpers import get_user

class BackendController(BaseController):
    def ping(self):
        id = request.POST['id']
        api_key = request.POST['api_key']

        try:
            conf = Session.query(Uploader).filter(Uploader.api_key==api_key).one().conference
        except Exception, e:
            print e
            return 'sorry, cannot find your api key'
        
        blipurl = 'http://blip.tv/file/%s/?skin=rss' % id

        try:
            x = Talk.import_blipurl(blipurl, conf)
            return 'imported: %d' % len(x)
        except KeyError, e:
            return 'sorry, the ID you provided does not seem to work. url tried: %s\n' % blipurl

        
