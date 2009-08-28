import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from hackertalks.lib.base import BaseController, render

from hackertalks.model import Talk
from hackertalks.model.meta import Session

log = logging.getLogger(__name__)

class FrontpageController(BaseController):
    def index(self):
        c.featured_talks = Session.query(Talk).order_by(Talk.recording_date.desc()).limit(25)
        return render('featured.jinja2')