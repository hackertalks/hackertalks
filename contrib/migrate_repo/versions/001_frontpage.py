import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base 

from migrate import *

Base = declarative_base()
Base.metadata.bind = migrate_engine

talks_speakers = sa.Table('talks_speakers', Base.metadata,
    sa.Column('talk_id', sa.types.Integer, sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer, sa.ForeignKey('speakers.id'), primary_key=True))

talks_featured = sa.Table('talks_featured', Base.metadata,
    sa.Column('talk_id', sa.types.Integer, sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('show_timestamp', sa.types.DateTime))


class Speaker(Base):
    __tablename__ = 'speakers'
 
    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Unicode)
    job_title = sa.Column(sa.types.Unicode)
    
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
    speakers = orm.relation('Speaker', secondary=talks_speakers, backref='talks')


def upgrade():    
    Speaker.__table__.create()
    Talk.__table__.create()
    talks_speakers.create()
    talks_featured.create()

def downgrade():
    talks_featured.drop()
    talks_speakers.drop()
    Talk.__table__.drop()
    Speaker.__table__.drop()