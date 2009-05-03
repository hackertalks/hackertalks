import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from hackertalks.lib.base import BaseController, render

from hackertalks.model import Talk
from hackertalks.model.meta import Session

log = logging.getLogger(__name__)

class TalkController(BaseController):

    def index(self, id):
	c.talk = Session.query(Talk).get(id)
        if (c.talk == None):
	    return render('/fourohfour.jinja2')
	else:
	    return render('/talk.jinja2')
