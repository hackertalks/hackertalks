"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from routes import url_for
