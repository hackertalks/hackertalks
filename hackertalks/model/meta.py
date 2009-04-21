"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.orm import scoped_session, sessionmaker
import elixir


__all__ = ['Session', 'engine', 'metadata']

# SQLAlchemy database engine. Updated by model.init_model()
engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

elixir.session = Session
elixir.options_defaults.update({
	    'shortnames': True
})

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = elixir.metadata
