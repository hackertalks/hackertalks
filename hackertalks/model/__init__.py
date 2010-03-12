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
    sa.Column('tag_id', sa.types.Integer(), sa.ForeignKey('tags.id'), primary_key=True), # this might be a bad idea.
    )

class Speaker(Base):
    __tablename__ = 'speakers'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    name = sa.Column(sa.types.Unicode())
    job_title = sa.Column(sa.types.Unicode())

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
    video_bliptv_id = sa.Column(sa.types.Integer(), unique=True)
    conference = sa.Column(sa.types.Unicode(), nullable=True)

    slug = sa.Column(sa.types.Unicode(), nullable=True, unique=True)

    ## We need a set list of licenses because they MUST be the same as where the videos are stored.
    license_id = sa.Column(sa.types.Integer(), sa.ForeignKey('licenses.id'))
    license = orm.relation(License, primaryjoin=license_id == License.id, backref="talks")
    
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')
    tags = orm.relation('Tag', secondary=talks_tags_table, backref='talks')

    def publish(self):
        if self.slug and self.id:
            return self

        speaker_names = u','.join(s.name for s in self.speakers)
        title = self.short_title if self.short_title else self.title
        base_slug = h.slugify(u'%s - %s' % (speaker_names, title))

        for x in xrange(10):
            meta.Session.begin_nested()
            m=u'%s%s' % (base_slug,x if x!=0 else u'')
            try:
                self.slug = m
                self.short_title = ''
                meta.Session.merge(self)
                meta.Session.commit()
                return self
            except:
                meta.Session.rollback()

    @property
    def url(self):
        return h.url_for('talk', slug=self.slug)

    @classmethod
    def online(self):
        return meta.Session.query(Talk).filter(Talk.slug!=None)

    
class FeaturedTalk(Base):
    """ past or future featured talks """
    __tablename__ = 'talks_featured'

    talk_id = sa.Column(sa.types.Integer(), sa.ForeignKey(Talk.id), nullable=False)
    date = sa.Column(sa.Date(), nullable=False, unique=True)

    talk = orm.relation(Talk, primaryjoin=talk_id == Talk.id, backref="featured")

    __table_args__ = (sa.PrimaryKeyConstraint("talk_id", "date"), {},)
    

class StumbleSession(Base):
    """ current or past record of an user stumblin' around
        we _could_ save the search params in here. just sayin'.
    """
    __tablename__ = 'stumble_session'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    session_id = sa.Column(sa.types.UnicodeText())
    human_id = sa.Column(sa.types.Integer(), sa.ForeignKey(Human.id), nullable=True)

    user = orm.relation(Human, primaryjoin=human_id == Human.id, backref='stumbles')


class StumbleVisit(Base):
    """ indicates that a session has seen a talk"""
    __tablename__ = 'stumble_session_talk'

    id = sa.Column(sa.types.Integer(), primary_key=True)

    stumble_session_id = sa.Column(sa.types.Integer(), sa.ForeignKey(StumbleSession.id))
    talk_id = sa.Column(sa.types.Integer(), sa.ForeignKey(Talk.id))

    talk = orm.relation(Talk, primaryjoin=talk_id == Talk.id, backref='visits')
    stumble_session = orm.relation(StumbleSession, primaryjoin=stumble_session_id == StumbleSession.id)


class Tag(Base):
    """ guess what: tags! """
    __tablename__ = 'tags'

    name = sa.Column(sa.types.Unicode(), unique=True) # this might be a bad idea.
    
    id = sa.Column(sa.types.Integer(), primary_key=True)

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
            x = meta.Session.query(Tag).filter(Tag.name==name).one()


