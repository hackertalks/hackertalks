import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from hackertalks.lib.base import BaseController, render

from hackertalks.model import Speaker
from hackertalks.model.meta import Session

log = logging.getLogger(__name__)

class SpeakerController(BaseController):

    q = Session.query(Speaker).order_by(Speaker.id.desc())
                                     
    def index(self):
        c.speakers = self.q.limit(25)
        return render('speaker/index.jinja2')
        
    def display(self, id):
        if id.isdigit():
            c.speaker = self.q.get(id)
            if c.speaker != None:
                return render('/speaker/display.jinja2')
            else:
                response.status_int = 404
                return render('/error.jinja2')
        response.status_int = 400
        return render('/error.jinja2')