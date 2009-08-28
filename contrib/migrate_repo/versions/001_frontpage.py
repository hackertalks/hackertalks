import sqlalchemy as sa
from sqlalchemy import orm

from migrate import *

metadata = sa.MetaData(migrate_engine)

talks = sa.Table('talks', metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('short_title', sa.types.String),
    sa.Column('title', sa.types.Text),
    sa.Column('description', sa.types.Text),
    sa.Column('thumbnail_url', sa.types.Text),
    sa.Column('recording_date', sa.types.Date),
    sa.Column('license', sa.types.Text),
    sa.Column('video_duration', sa.types.Interval),
    sa.Column('video_embedcode', sa.types.Text),
    sa.Column('video_bliptv_id', sa.types.Integer))

speakers = sa.Table('speakers', metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('name', sa.types.String),
    sa.Column('job_title', sa.types.String))

talks_speakers = sa.Table('talks_speakers', metadata,
    sa.Column('talk_id', sa.types.Integer, sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer, sa.ForeignKey('speakers.id'), primary_key=True))

talks_featured = sa.Table('talks_featured', metadata,
    sa.Column('talk_id', sa.types.Integer, sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('show_timestamp', sa.types.DateTime))

def upgrade():    
    speakers.create()
    talks.create()
    talks_speakers.create()
    talks_featured.create()

def downgrade():
    talks_featured.drop()
    talks_speakers.drop()
    talks.drop()
    speakers.drop()