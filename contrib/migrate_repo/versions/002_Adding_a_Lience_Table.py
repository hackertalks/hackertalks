import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base 

from migrate import *

Base = declarative_base()
Base.metadata.bind = migrate_engine

talks_speakers_table = sa.Table('talks_speakers', Base.metadata,
    sa.Column('talk_id', sa.types.Integer(), sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer(), sa.ForeignKey('speakers.id'), primary_key=True),
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
    video_bliptv_id = sa.Column(sa.types.Integer())
    license = sa.Column(sa.types.Integer(), sa.ForeignKey('licenses.id'))
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')
    


def upgrade():
    License.__table__.create()
    conn = migrate_engine.connect()
    conn.execute("ALTER TABLE talks DROP COLUMN license")
    conn.execute("ALTER TABLE talks ADD license INTEGER")
    conn.execute("ALTER TABLE talks ADD CONSTRAINT talks_license_fkey FOREIGN KEY(license) REFERENCES licenses (id)")

def downgrade():
    conn = migrate_engine.connect()
    conn.execute("ALTER TABLE talks DROP CONSTRAINT talks_license_fkey")
    conn.execute("ALTER TABLE talks DROP COLUMN license")
    conn.execute("ALTER TABLE talks ADD license TEXT")
    License.__table__.drop()
