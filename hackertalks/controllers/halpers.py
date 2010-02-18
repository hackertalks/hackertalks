from hackertalks.model import Tag
from hackertalks.model.meta import Session
from decorator import decorator
from pylons.decorators.util import get_pylons


def has_taglist():
    def inner(func, *args, **kwargs):
        pylons = get_pylons(args)
        pylons.c.tags = Session.query(Tag).all()
        return func(*args, **kwargs)
    return decorator(inner)
