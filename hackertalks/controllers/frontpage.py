import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from hackertalks.lib.base import BaseController, render

from hackertalks.model import FeaturedTalk, Talk
from hackertalks.model.meta import Session
from datetime import datetime
from hackertalks.controllers.halpers import get_user

log = logging.getLogger(__name__)

class FrontpageController(BaseController):
    def __before__(self):
        request.user = get_user(session)

    def index(self):
        c.featured_talks = [x.talk for x in Session.query(FeaturedTalk).filter(FeaturedTalk.date<=datetime.now()).order_by(FeaturedTalk.date.desc()).limit(7)]

        session['current'] = None
        session.save()

        return render('featured.jinja2')
