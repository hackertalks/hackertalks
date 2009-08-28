"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import datetime

from hackertalks.model import meta

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

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode)
    job_title = sa.Column(sa.types.Unicode)

    def __init__(self, name, job_title):
        self.name = name
        self.job_title = job_title

    def __repr__(self):
        return "<Speaker(id='%d', name='%s')>" % (self.id, self.name)

class Talk(Base):
    __tablename__ = 'talks'

    id = sa.Column(sa.types.Integer, primary_key=True)
    short_title = sa.Column(sa.types.Unicode)
    title = sa.Column(sa.types.UnicodeText)
    description = sa.Column(sa.types.UnicodeText)
    thumbnail_url = sa.Column(sa.types.UnicodeText)
    recording_date = sa.Column(sa.types.Date)
    license = sa.Column(sa.types.UnicodeText)
    video_duration = sa.Column(sa.types.Interval)
    video_embedcode = sa.Column(sa.types.UnicodeText)
    video_bliptv_id = sa.Column(sa.types.Integer)
    
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')

    def __init__(self, short_title, title, description, thumbnail_url, recording_date, license, video_duration, video_embedcode, video_bliptv_id):
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
