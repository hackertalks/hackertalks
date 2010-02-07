"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['Session', 'engine', 'metadata']

# SQLAlchemy database engine. Updated by model.init_model()
engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database


class HTBase(object):
    def __repr__(self):
        s = "<"
        s += self.__class__.__name__
        s += "("
        s += '.'.join(['%s="%s"' % (key, unicode(self.__dict__.get(key, getattr(self, key, '__unknown__')))) for key in self.__table__.columns.keys()])
        s += ")>"
        return s

    def __getattr__(self, **kwargs):
        return Base.__getattr__(**kwargs)

Base = declarative_base(cls=HTBase)

metadata = Base.metadata
