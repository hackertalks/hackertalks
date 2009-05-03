"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    sa.Column('talk_id', sa.types.Integer(), sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('tag_id', sa.types.Integer(), sa.ForeignKey('tags.id'), primary_key=True),
    )

talks_speakers_table = sa.Table('talks_speakers', meta.metadata,
    sa.Column('talk_id', sa.types.Integer(), sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer(), sa.ForeignKey('speakers.id'), primary_key=True),
    )

class TalkType(Base):
    __tablename__ = 'talk_types'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    type = sa.Column(sa.types.Unicode())

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return "<TalkType('%s')>" % (self.type)


class Tag(Base):
    __tablename__ = 'tags'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    tag = sa.Column(sa.types.Unicode())

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return "<Tag('%s')>" % (self.tag)

class Speaker(Base):
    __tablename__ = 'speakers'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    first_name = sa.Column(sa.types.Unicode())
    last_name = sa.Column(sa.types.Unicode())
    nickname = sa.Column(sa.types.Unicode())

    def __init__(self, first_name, last_name, nickname):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname

    def __repr__(self):
            return "<Speaker('%s',  '%s', '%s')>" % (self.first_name, self.last_name, self.nickname)

class Language(Base):
    __tablename__ = 'languages'

    code = sa.Column(sa.types.Unicode(), primary_key=True)
    name = sa.Column(sa.types.Unicode())

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return "<Lanuage('%s', '%s')>" % (self.code, self.name)

class Talk(Base):
    __tablename__ = 'talks'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    title = sa.Column(sa.types.Unicode())
    description = sa.Column(sa.types.UnicodeText())
    video_length = sa.Column(sa.types.Interval())
    video_embedcode = sa.Column(sa.types.Unicode())
    # Many To One Columns
    language_code = sa.Column(sa.types.Unicode(), sa.ForeignKey('languages.code'))
    type_id = sa.Column(sa.types.Integer(), sa.ForeignKey('talk_types.id'))
    #Many to One Relationships
    type = orm.relation(TalkType, backref=orm.backref('talk_types', order_by=id))
    language = orm.relation(Language, backref=orm.backref('languages', order_by=id))
    #Many to Many  Relationships
    tags =  orm.relation('Tag', secondary=talks_tags_table, backref='talks')
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')

    def __init__(self, title, description, language_code, length):
        self.title = title
        self.description = description
        self.length = length

    def __repr__(self):
        return "<Talk('%s', '%s', '%s', '%s', '%s')>" % (self.title, self.description, self.length, self.type, self.language)

