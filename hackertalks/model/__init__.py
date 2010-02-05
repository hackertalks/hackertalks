"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
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

class Speaker(Base):
    __tablename__ = 'speakers'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    name = sa.Column(sa.types.Unicode())
    job_title = sa.Column(sa.types.Unicode())

    def __init__(self, name, job_title):
        self.name = name
        self.job_title = job_title

    def __repr__(self):
        return "<Speaker(id='%d', name='%s')>" % (self.id, self.name)
    
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
    
    def __init__(self, name=u'undef', shortname=u'undef', abbreviation=u'undef', link=u'undef', thumbnail=u'undef', shareable=u'undef', description=u'undef'):
        self.name = name
        self.shortname = shortname
        self.abbreviation = abbreviation
        self.link = link
        self.thumbnail = thumbnail
        self.shareable = shareable
        self.description = description
        
    def __repr__(self):
        return "<License(id='%d', name='%s')>" % (self.id, self.name)
    pass


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

    ## We need a set list of licenses because they MUST be the same as where the videos are stored.
    license = sa.Column(sa.types.Integer(), sa.ForeignKey('licenses.id'))
    
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')

    def __init__(self, short_title=u'undef', title=u'undef', description=u'undef', thumbnail_url=u'undef', recording_date=datetime.datetime.now(), license=None, video_duration=datetime.timedelta(0), video_embedcode=u'undef', video_bliptv_id=u'undef'):
        self.short_title = short_title
        self.title = title
        self.description = description
        self.thumbnail_url = thumbnail_url
        self.recording_date = recording_date
        self.license = license
        self.video_duration = video_duration
        self.video_embedcode = video_embedcode
        self.video_bliptv_id = video_bliptv_id

    def __repr__(self):
        return "<Talk(id='%s', title='%s', video_bliptv_id='%s')>" % (self.id, self.title, self.video_bliptv_id)
    
class FeaturedTalk(Base):
    __tablename__ = 'talks_featured'

    talk_id = sa.Column(sa.types.Integer(), sa.ForeignKey(Talk.id), nullable=False)
    date = sa.Column(sa.Date(), nullable=False, unique=True)

    talk = orm.relation(Talk, primaryjoin=talk_id == Talk.id)

    __table_args__ = (sa.PrimaryKeyConstraint("talk_id", "date"), {},)


