"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from hackertalks.model import meta

Base = meta.Base

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine
    meta.metadata.bind = engine


talks_tags_table = sa.Table('talks_tags', meta.metadata,
    sa.Column('talk_id', sa.types.Integer, sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('tag_id', sa.types.Integer, sa.ForeignKey('tags.id'), primary_key=True),
    )

talks_speakers_table = sa.Table('talks_speakers', meta.metadata,
    sa.Column('talk_id', sa.types.Integer, sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer, sa.ForeignKey('speakers.id'), primary_key=True),
    )

class Talk(Base):
    __tablename__ = 'talks'

    id = sa.Column(sa.types.Integer, primary_key=True)
    title = sa.Column(sa.types.String)
    description = sa.Column(sa.types.String)
    language_code = sa.Column(sa.types.String)
    video_length = sa.Column(sa.types.String)
    video_embedcode = sa.Column(sa.types.String)

    tags =  orm.relation('Tag', secondary=talks_tags_table, backref='talks')
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='posts')

    def __init__(self, title, description, language_code, video_length, video_embedcode):
        self.title = title
        self.description = description
        self.language_code = language_code
        self.video_length = video_length
        self.video_embedcode = video_embedcode

    def __repr__(self):
        return "<Talk('%s', '%s', '%s', '%s', '%s')>" % (self.title, self.description, self.language_code, self.video_length, self.video_embedcode)

class Tag(Base):
    __tablename__ = 'tags'

    id = sa.Column(sa.types.Integer, primary_key=True)
    tag = sa.Column(sa.types.String)

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return "<Tag('%s')>" % (self.tag)
        
class Speaker(Base):
    __tablename__ = 'speakers'

    id = sa.Column(sa.types.Integer, primary_key=True)
    first_name = sa.Column(sa.types.String)
    last_name = sa.Column(sa.types.String)
    nickname = sa.Column(sa.types.String)

    def __init__(self, first_name, last_name, nickname):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname

    def __repr__(self):
            return "<Speaker('%s',  '%s', '%s')>" % (self.first_name, self.last_name, self.nickname)

class Language(Base):
    __tablename__ = 'languages'

    code = sa.Column(sa.types.String, primary_key=True)
    name = sa.Column(sa.types.String)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return "<Lanuage('%s', '%s')>" % (self.code, self.name)


