import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from hackertalks.lib.base import BaseController, render

from hackertalks.model import FeaturedTalk, Talk
from hackertalks.model.meta import Session
from datetime import datetime

log = logging.getLogger(__name__)

class FrontpageController(BaseController):
    def index(self):

        print '---'
        print 'logged_in' in session
        print '---'

        c.featured_talks = [x.talk for x in Session.query(FeaturedTalk).filter(FeaturedTalk.date<=datetime.now()).order_by(FeaturedTalk.date.desc()).limit(7)]
        return render('featured.jinja2')
