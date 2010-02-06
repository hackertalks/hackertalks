import os
import md5
import sha
from datetime import datetime

import pylons
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from hackertalks.model import meta

Base = meta.Base

class Human(Base):
    """Represents a human user"""

    __tablename__ = 'human'

    id = sa.Column(sa.types.Integer(), primary_key=True)

    displayname = sa.Column(sa.types.UnicodeText())
    email = sa.Column(sa.types.UnicodeText(), unique=True)
    timezone = sa.Column(sa.types.UnicodeText())
    password = sa.Column(sa.types.UnicodeText())
    created = sa.Column(sa.types.DateTime(), default=datetime.utcnow)
    last_login = sa.Column(sa.types.DateTime(), default=datetime.utcnow)
    blog = sa.Column(sa.types.UnicodeText())
    session_id = sa.Column(sa.types.UnicodeText())
    
    email_token = sa.Column(sa.types.UnicodeText())
    password_token = sa.Column(sa.types.UnicodeText())
    
    email_token_issue = sa.Column(sa.types.DateTime())
    password_token_issue = sa.Column(sa.types.DateTime())
    
    @staticmethod
    def hash_password(plain_text):
        """Returns a crypted/salted password field
        
        The salt is stored in front of the password, for per user 
        salts.
        
        """
        if isinstance(plain_text, unicode):
            plain_text = plain_text.encode('utf-8')
        password_salt = sha.new(os.urandom(60)).hexdigest()
        crypt = sha.new(plain_text + password_salt).hexdigest()
        return password_salt + crypt
    
    def verify_password(self, plain_text):
        """Verify a plain text string is the users password"""  
        if isinstance(plain_text, unicode):
            plain_text = plain_text.encode('utf-8')
        
        # Some users don't have passwords, like OpenID users, so they
        # can't use a password to login
        if not self.password:
            return False
        
        password_salt = self.password[:40]
        crypt_pass = sha.new(plain_text + password_salt).hexdigest()
        if crypt_pass == self.password[40:]:
            return True
        else:
            return False
    
    def email_hash(self):
        return md5.md5(self.email).hexdigest()
    
    def generate_token(self):
        """Generate's a token for use either for forgot password or
        email verification"""
        return sha.new(os.urandom(60)).hexdigest()
    
    def valid_password_token(self):
        diff = datetime.now() - self.password_token_issue
        token_lifespan = pylons.config['sso.password_token_lifespan']
        if diff.days < 1 and diff.seconds < token_lifespan:
            return True
        else:
            return False
    
    def in_group(self, group):
        if group in list(self.groups):
            return True
        else:
            return False
    
    def process_login(self):
        session = pylons.session._current_obj()
        session['logged_in'] = True
        session['displayname'] = self.displayname
        session['user_id'] = self.id
        session.save()
        self.session_id = session.id
        meta.Session.commit()

    @property
    def openids(self):
        return meta.Session.query(OpenID).filter(OpenID.human==self).all()


class OpenID(Base):
    """openid"""

    __tablename__ = 'openid'

    openid = sa.Column(sa.types.UnicodeText(), primary_key=True)
    human = sa.ForeignKey(Human)
