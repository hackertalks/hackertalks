from datetime import datetime
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest, secure, jsonify
from tw.mods.pylonshf import validate


from hackertalks.lib.base import BaseController, render_mako
from hackertalks.lib.helpers import failure_flash, success_flash
from hackertalks.lib.mail import EmailMessage
from hackertalks.model import Human, forms
from hackertalks.model.meta import Session
from hackertalks.controllers.halpers import get_user

log = logging.getLogger(__name__)


class AccountsController(BaseController):
    def __before__(self):
        c.active_tab = True
        c.active_sub = True
        request.user = get_user(session)

    @rest.dispatch_on(POST='_forgot_password')
    def forgot_password(self):
        return render_mako('/accounts/forgot_password.mako')
    
    def verify_email(self, token):
        users = Session.query(Human).filter(Human.email_token==token).all()
        if users:
            user = users[0]
            
            # If there's a email token issue (change email address), verify
            # its still valid
            if user.email_token_issue:
                diff = datetime.utcnow() - user.email_token_issue
                if diff.days > 1 or diff.seconds > 3600:
                    failure_flash('This e-mail verification token has expired.')
                    redirect_to('home')
            
            # Valid e-mail token, remove it and log the user in
            user.email_token = user.email_token_issue = None
            user.process_login()
            success_flash('Your email has been verified, and you have been'
                          ' logged into PylonsHQ')
            redirect_to('home')
        else:
            # No valid e-mail token
            failure_flash('Invalid e-mail token')
            redirect_to('home')
    
    @validate(form=forms.forgot_password_form, error_handler='forgot_password')
    @secure.authenticate_form
    def _forgot_password(self):
        user = Session.query(Human).filter(Human.email==self.form_result['email_address']).one()
        user.password_token = user.generate_token()
        c.password_token = user.password_token
        user.password_token_issue = datetime.utcnow()
        Session.commit()

        message = EmailMessage(subject="PylonsHQ - Lost Password", 
                               body=render_mako('/email/lost_password.mako'),
                               from_email="PylonsHQ <pylonshq@groovie.org>",
                               to=[self.form_result['email_address']])
        message.send(fail_silently=True)
        success_flash('An e-mail has been sent to your account to verify the password reset request.')
        redirect_to('account_login')
    
    @rest.dispatch_on(POST='_change_password')
    def change_password(self, token):
        users = Session.query(Human).filter(Human.password_token==token).all()
        if not users:
            failure_flash('That password token is no longer valid.')
            redirect_to('account_login')
        
        user = users[0]
        diff = datetime.utcnow() - user.password_token_issue
        if diff.days > 1 or diff.seconds > 3600:
            failure_flash('Password token is no longer valid, please make a new password reset request.')
            redirect_to('forgot_password')
        return render_mako('/accounts/change_password.mako')
    
    @validate(form=forms.change_password_form, error_handler='change_password')
    @secure.authenticate_form
    def _change_password(self, token):
        users = Session.query(Human).filter(Human.password_token==token).all() or abort(401)
        user = users[0]
        diff = datetime.utcnow() - user.password_token_issue
        if diff.days > 1 or diff.seconds > 3600:
            failure_flash('Password token is no longer valid, please make a new password reset request.')
            redirect_to('forgot_password')
        user.password_token = user.password_token_issue = None
        user.password = user.hash_password(self.form_result['password'])
        Session.commit()

        success_flash('Your password has been reset successfully')
        redirect_to('account_login')

    def logout(self):
        request.user.session_id = None
        Session.commit()
        session.clear()
        session.save()
        redir = request.GET.get('redir')
        success_flash('You have logged out of your session')
        if redir:
            redirect_to(str(redir))
        else:
            redirect_to('home')
    
    @rest.dispatch_on(POST='_process_login')
    def login(self):
        redir = request.GET.get('redir')
        if redir and redir.startswith('/') and redir != url('account_login'):
            session['redirect'] = str(redir)
            session.save()
        return render_mako('/accounts/login.mako')
    
    @validate(form=forms.login_form, error_handler='login')
    @secure.authenticate_form
    def _process_login(self):
        user = self.form_result['user']
        user.process_login()        
        success_flash('You have logged into PylonsHQ')
        if session.get('redirect'):
            redir_url = session.pop('redirect')
            session.save()
            redirect_to(redir_url)
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_openid_associate')
    def openid_associate(self):
        openid_url = session.get('openid_identity')
        if not openid_url:
            redirect_to('account_register')
        c.openid = openid_url
        return render_mako('/accounts/associate.mako')
    
    @validate(form=forms.login_form, error_handler='login')
    def _process_openid_associate(self):
        openid_url = session.get('openid_identity')
        user = self.form_result['user']
        oi = OpenID()
        oi.openid = openid_url
        oi.user = user
        Session.add(oi)
        Session.commit()
        user.process_login()
        success_flash('You have associated your OpenID to your account, and signed in')
        if session.get('redirect'):
            redir_url = session.pop('redirect')
            session.save()
            redirect_to(redir_url)
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_openid_registration')
    def openid_register(self):
        openid_url = session.get('openid_identity')
        if not openid_url:
            redirect_to('account_register')
        c.openid = session.get('openid_identity')
        c.defaults = {}
        return render_mako('/accounts/register.mako')
    
    @validate(form=forms.openid_registration_form, error_handler='openid_register')
    def _process_openid_registration(self):
        new_user = Human(displayname=self.form_result['displayname'],
                         timezone = self.form_result['timezone'],
                         email=self.form_result['email_address'])
        oi = OpenID()
        oi.openid = session['openid_identity']
        oi.user = new_user
        Session.add(oi)
        return self._finish_registration(new_user)
    
    @rest.dispatch_on(POST='_process_registration')
    def register(self):
        c.openid = None
        return render_mako('/accounts/register.mako')

    @validate(form=forms.registration_form, error_handler='register')
    @secure.authenticate_form
    def _process_registration(self):
        new_user = Human(displayname=self.form_result['displayname'],
                         timezone = self.form_result['timezone'],
                         email=self.form_result['email_address'])
        new_user.password = Human.hash_password(self.form_result['password'])
        return self._finish_registration(new_user)
    
    def _finish_registration(self, user):
        user.email_token = c.email_token = user.generate_token()
        user.email_token_issue = datetime.utcnow()
        Session.add(user)
        Session.commit()
        
        
        # Send out the welcome email with the reg token
        message = EmailMessage(subject="PylonsHQ - Registration Confirmation",
                               body=render_mako('/email/register.mako'),
                               from_email="PylonsHQ <pylonshq@groovie.org>",
                               to=[self.form_result['email_address']])
        message.send(fail_silently=True)
        
        success_flash("User account '%s' created successfully. An e-mail has"
                      " been sent to activate your account." % user.displayname)
        redirect_to('home')
