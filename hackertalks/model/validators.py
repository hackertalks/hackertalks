"""Custom validators"""
import re
from datetime import datetime

import formencode
import pylons

from hackertalks.model import Human
from hackertalks.model.meta import Session


class ExistingEmail(formencode.FancyValidator):
    def _to_python(self, value, state):
        users = Session.query(Human).filter(Human.email==value).all()
        if not users:
            raise formencode.Invalid('No such e-mail address was found',
                                     value, state)
        user = users[0]
        
        # Check to see if the user has recently asked for an email token
        if user.password_token_issue:
            diff = datetime.utcnow() - user.password_token_issue
            if diff.days < 1 and diff.seconds < 3600:
                raise formencode.Invalid(
                    "You've already requested a password recently.  Please " 
                    "wait and try later.", value, state)
        return value


class UniqueDisplayname(formencode.FancyValidator):
    def _to_python(self, value, state):
        users = Session.query(Human).filter(Human.displayname==value).all()
        if users:
            raise formencode.Invalid('Display name already exists',
                                     value, state)
        else:
            return value


class UniqueEmail(formencode.FancyValidator):
    def _to_python(self, value, state):
        users = Session.query(Human).filter(Human.email==value).all()
        if users:
            raise formencode.Invalid('Email address already exists', value,
                                     state)
        else:
            return value


class ValidPassword(formencode.FancyValidator):
    def _to_python(self, value, state):
        if len(value) < 6:
            raise formencode.Invalid('Password is too short, must be at least'
                                     ' 6 characters', value, state)
        return value


class ValidLogin(formencode.FancyValidator):
    field_names = None
    validate_partial_form = False
    email = None
    answer = None
    password = None

    messages = {
        'badlogin': "Invalid email and/or password",
    }
    
    def validate_python(self, field_dict, state):
        errors = {}
        email = field_dict[self.email]
        password = field_dict[self.password]
        
        users = Session.query(Human).filter(Human.email==email).all()
        if users:
            user = users[0]
        else:
            user = None
        
        if not user:
            errors[self.email] = self.message('badlogin', state)
        if not errors:
            valid_password = user.verify_password(password)
            if valid_password:
                field_dict['user'] = user
            else:
                errors[self.email] = self.message('badlogin', state)
        if errors:
            error_list = errors.items()
            error_list.sort()
            error_message = '<br>\n'.join(
                ['%s: %s' % (name, value) for name, value in error_list])
            raise formencode.Invalid(error_message,
                                     field_dict, state,
                                     error_dict=errors)
