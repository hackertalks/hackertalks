"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from hackertalks.lib import helpers as h
from sqlalchemy.ext.declarative import declarative_base
import datetime

from hackertalks.model import meta
from hackertalks.model.human import Human, OpenID

Base = meta.Base

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine
    meta.metadata.bind = engine

talks_speakers_table = sa.Table('talks_speakers', meta.metadata,
    sa.Column('talk_id', sa.types.Integer(), sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer(), sa.ForeignKey('speakers.id'), primary_key=True),
    )

talks_tags_table = sa.Table('talks_tags', meta.metadata,
    sa.Column('talk_id', sa.types.Integer(), sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('tag_name', sa.types.Unicode(), sa.ForeignKey('tags.name'), primary_key=True), # this might be a bad idea.
    )

class Speaker(Base):
    __tablename__ = 'speakers'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    name = sa.Column(sa.types.Unicode())
    job_title = sa.Column(sa.types.Unicode())

#    def __init__(self, name, job_title):
#        self.name = name
#        self.job_title = job_title

    
class License(Base):
    __tablename__ = 'licenses'
    
    id = sa.Column(sa.types.Integer(), primary_key=True)
    name = sa.Column(sa.types.Unicode())
    shortname = sa.Column(sa.types.Unicode())
    abbreviation = sa.Column(sa.types.Unicode())
    link = sa.Column(sa.types.Unicode())
    thumbnail = sa.Column(sa.types.Unicode())
    shareable = sa.Column(sa.types.Boolean())
    description = sa.Column(sa.types.UnicodeText())
    
#    def __init__(self, name=None, shortname=None, abbreviation=None, link=None, thumbnail=None, shareable=None, description=None):
#        self.name = name
#        self.shortname = shortname
#        self.abbreviation = abbreviation
#        self.link = link
#        self.thumbnail = thumbnail
#        self.shareable = shareable
#        self.description = description
        

class Talk(Base):
    __tablename__ = 'talks'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    short_title = sa.Column(sa.types.Unicode())
    title = sa.Column(sa.types.Unicode())
    description = sa.Column(sa.types.UnicodeText())
    thumbnail_url = sa.Column(sa.types.Unicode())
    recording_date = sa.Column(sa.types.Date())
    video_duration = sa.Column(sa.types.Interval())
    video_embedcode = sa.Column(sa.types.UnicodeText())
    video_bliptv_id = sa.Column(sa.types.Integer())

    slug = sa.Column(sa.types.Unicode(), nullable=True, unique=True)

    ## We need a set list of licenses because they MUST be the same as where the videos are stored.
    license = sa.Column(sa.types.Integer(), sa.ForeignKey('licenses.id'))
    
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')

#    def __init__(self, short_title=None, title=None, description=None, thumbnail_url=None, recording_date=datetime.datetime.now(), license=None, video_duration=datetime.timedelta(0), video_embedcode=None, video_bliptv_id=None):
#        self.short_title = short_title
#        self.title = title
#        self.description = description
#        self.thumbnail_url = thumbnail_url
#        self.recording_date = recording_date
#        self.license = license
#        self.video_duration = video_duration
#        self.video_embedcode = video_embedcode
#        self.video_bliptv_id = video_bliptv_id

    def publish(self):
        speaker_names = u','.join(s.name for s in self.speakers)
        title = self.short_title if self.short_title else self.title
        base_slug = h.slugify(u'%s - %s' % (speaker_names, title))

        for x in xrange(10):
            meta.Session.begin_nested()
            m=u'%s%s' % (base_slug,x if x!=0 else u'')
            try:
                self.slug = m
                meta.Session.merge(self)
                meta.Session.commit()
                return self
            except:
                meta.Session.rollback()

    @property
    def url(self):
        return h.url_for('talk', slug=self.slug)

    
class FeaturedTalk(Base):
    """ past or future featured talks """
    __tablename__ = 'talks_featured'

    talk_id = sa.Column(sa.types.Integer(), sa.ForeignKey(Talk.id), nullable=False)
    date = sa.Column(sa.Date(), nullable=False, unique=True)

    talk = orm.relation(Talk, primaryjoin=talk_id == Talk.id)

    __table_args__ = (sa.PrimaryKeyConstraint("talk_id", "date"), {},)
    

class StumbleSession(Base):
    """ current or past record of an user stumblin' around """
    __tablename__ = 'stumble_session'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    session_id = sa.Column(sa.types.UnicodeText())


class StumbleVisit(Base):
    """ indicates that a session has seen a talk"""
    __tablename__ = 'stumble_session_talk'

    id = sa.Column(sa.types.Integer(), primary_key=True)

    stumble_session_id = sa.Column(sa.types.Integer(), sa.ForeignKey(StumbleSession.id))
    talk_id = sa.Column(sa.types.Integer(), sa.ForeignKey(Talk.id))

    talk = orm.relation(Talk, primaryjoin=talk_id == Talk.id)
    stumble_session = orm.relation(StumbleSession, primaryjoin=stumble_session_id == StumbleSession.id)


class Tag(Base):
    """ guess what: tags! """
    __tablename__ = 'tags'

    name = sa.Column(sa.types.Unicode(), primary_key=True) # this might be a bad idea.

    @classmethod
    def get_or_create(cls, name):
        try:
            meta.Session.begin_nested()
            x = Tag()
            x.name = name
            meta.Session.add(x)
            meta.Session.commit()
        except sa.exceptions.SQLAlchemyError, e: # IntegrityError and FlushError encountered
            meta.Session.rollback()
            return meta.Session.query(Tag).filter(Tag.name==name).one()

