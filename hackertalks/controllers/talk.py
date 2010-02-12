import logging

from sqlalchemy import or_, func

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from hackertalks.lib.base import BaseController, render

from hackertalks.model import Talk
from hackertalks.model.meta import Session

log = logging.getLogger(__name__)

class TalkController(BaseController):
    q = Session.query(Talk).order_by(Talk.id.desc())
                                     
    def index(self):
        c.talks = self.q.limit(25)
        return render('talk/index.jinja2')
        
    def display(self, slug, context=None):
        print context
        c.talk = self.q.filter(Talk.slug == slug).all()[0]
        if c.talk != None:
            return render('/talk/display.jinja2')
        else:
            response.status_int = 404
            return render('/error.jinja2')
    
    def feed(self):
        talks = self.q.limit(10)
        feed = Rss201rev2Feed(
            title=u'Hackertalks New Talks Feed',
            link=url_for(),
            description=u'Hackertalks New Talks Feed',
            language=u'en',
        )
        for talk in talks:
            feed.add_item(title=talk.subject,
                link=talk.url,
                description=talk.content,
                ## pubdate=talk.date,
                author_name=talk.author,
            )
        response.content_type = u'application/rss+xml'
        return feed.writeString('utf-8')

    def searchpoint(self):
        s = request.GET.get('search','').lower()
        s = s.replace('/','_')
        return redirect_to(action='search', kw=s)


    def search(self, kw):
        talks = self.q.filter(or_(func.lower(Talk.title).contains(kw),func.lower(Talk.description).contains(kw))).all()

        c.talks = talks
        
        return render('/talk/search.jinja2')

