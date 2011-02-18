"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.pylonslib.secure_form import secure_form
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.pylonslib import Flash as _Flash
from pylons import session, url
import re
from markdown import markdown
from hackertalks.model import meta, forms as accountforms
from hackertalks import model
import sqlalchemy as sa
from globalhelpers import *
import email

success_flash = _Flash('success')
failure_flash = _Flash('failure')

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

def format_duration(delta):
    seconds = delta.seconds
    minutes = seconds / 60
    
    if minutes >= 60:
        return '%d:%02d h' % (minutes / 60, minutes % 60)
    else:
        return '%d:%02d min' % (minutes, seconds % 60)

def popular_tags():
    q = meta.Session.query(model.Tag,sa.func.count('*')).join(model.talks_tags_table).group_by(model.Tag.name, model.Tag.id).order_by(sa.desc('count_1'))

    return [x[0] for x in q[:15]]
