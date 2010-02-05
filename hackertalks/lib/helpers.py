"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.pylonslib.secure_form import secure_form
from routes import url_for, url_for as url
from webhelpers.pylonslib import Flash as _Flash
from pylons import session

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
