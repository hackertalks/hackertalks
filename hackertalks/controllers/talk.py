import logging

from sqlalchemy import or_, func

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from hackertalks.lib.base import BaseController, render

from hackertalks.model import Talk, StumbleSession, StumbleVisit, Tag
from hackertalks.model.meta import Session
from hackertalks.controllers.halpers import has_taglist

import datetime

log = logging.getLogger(__name__)

class TalkController(BaseController):
    q = Session.query(Talk).order_by(Talk.id.desc())
                                     
    @has_taglist()
    def index(self):
        c.talks = self.q.limit(25)
        return render('talk/index.jinja2')
        
    @has_taglist()
    def display(self, slug, context=None):
        
        print session.get('current', '')

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

    @has_taglist()
    def searchpoint(self):
        s = request.GET.get('search','').lower()
        s = s.replace('/','_')
        return redirect_to(action='search', kw=s)


    @has_taglist()
    def search(self, kw):
        talks = self.q.filter(or_(func.lower(Talk.title).contains(kw),func.lower(Talk.description).contains(kw))).all()

        c.talks = talks

        session['current'] = {'type': 'search',
                'term': kw
                }
        session.save()
        
        return render('/talk/search.jinja2')

    def stumble(self):
        ss = StumbleSession()
        Session.add(ss)
        Session.flush()
        session['current'] = {'type': 'stumble',
                'duration': [datetime.timedelta(minutes=int(request.POST['duration_start'])),
                    datetime.timedelta(minutes=int(request.POST['duration_end']))],
                'tags': request.POST.getall('tag'),
                'ssid': ss.id,
                }
        session.save()
        Session.commit()
        redirect_to(url_for('talk_stumble_next'))

    def stumble_next(self):
        curr = session.get('current', None)
        if not curr:
            return 'no stumble session!'

        ss = Session.query(StumbleSession).get(curr['ssid'])

        ts = Session.query(Talk).filter(Talk.video_duration\
                .between(curr['duration'][0],
                         curr['duration'][1]
                         )
                ).join(Talk.tags).filter(
                        Tag.name.in_(curr['tags'])
                )
        # TODO: filter if use has ever visited the talk. not only in this session

        for t in ts:
            if not [x for x in t.visits if x.stumble_session==ss]:
                sv = StumbleVisit(talk=t, stumble_session=ss)
                Session.add(sv)
                Session.commit()
                redirect_to(t.url)
        
        session['current'] = None
        session.save()
        return 'zomg no moar stumbling!'
        
