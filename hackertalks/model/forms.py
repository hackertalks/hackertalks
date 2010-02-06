from formencode import All, Schema
from formencode.validators import FieldsMatch
from tw import forms
from tw.api import WidgetsList
from tw.forms.validators import DateTimeConverter, UnicodeString, Email, OneOf
import pytz

#from kai.lib.highlight import langdict
#from kai.model.validators import ExistingSnippetTitle, ExistingEmail, UniqueDisplayname, UniqueEmail, ValidLogin, ValidPassword
from hackertalks.model.validators import ExistingEmail, UniqueDisplayname, UniqueEmail, ValidLogin, ValidPassword

forms.FormField.engine_name = "mako"

class FilteringSchema(Schema):
    filter_extra_fields = False
    allow_extra_fields = True
    ignore_key_missing = False


class AutoComplete(forms.TextField):
    template = 'hackertalks.templates.widgets.autocomplete'


class SecureToken(forms.HiddenField):
    template = 'hackertalks.templates.widgets.secure'


class BotsAreLame(forms.HiddenField):
    template = 'hackertalks.templates.widgets.notabot'

#
#class CommentForm(forms.TableForm):
#    class fields(WidgetsList):
#        comment = forms.TextArea(
#            validator = UnicodeString(not_empty=True))
#        preview = forms.Button(
#            name='Preview',
#            attrs={'value':'Preview'})
#comment_form = CommentForm('comment_form')
#
#
#class SnippetForm(forms.TableForm):
#    class fields(WidgetsList):
#        title = forms.TextField(
#            validator = ExistingSnippetTitle(not_empty=True))
#        description = forms.TextArea(
#            help_text = "ONE paragraphs summarizing the snippet. NO FORMATTING IS APPLIED",
#            validator = UnicodeString())
#        content = forms.TextArea(
#            help_text = "The full content of the snippet. Restructured Text formatting is used.",
#            validator = UnicodeString(not_empty=True))
#        tags = AutoComplete(
#            validator = UnicodeString())
#        preview = forms.Button(
#            name='Preview',
#            attrs={'value':'Preview'})
#snippet_form = SnippetForm('snippet_form')
#
#
#class PastebinForm(forms.TableForm):
#    class fields(WidgetsList):
#        title = forms.TextField(
#            validator = UnicodeString(not_empty=True))
#        language = forms.SingleSelectField(
#            options = sorted(langdict.items(), cmp=lambda x,y: cmp(x[1], y[1])),
#            validator = OneOf(langdict.keys(), not_empty=True))
#        code = forms.TextArea(
#            validator = UnicodeString(not_empty=True))
#        tags = AutoComplete(
#            validator = UnicodeString(not_empty=False))
#        notabot = BotsAreLame(
#            validator = UnicodeString(not_empty=True),
#            attrs = {'value':'most_likely'})
#pastebin_form = PastebinForm('pastebin_form')
#
#
#class NewArticleForm(forms.TableForm):
#    class fields(WidgetsList):
#        title = forms.TextField(
#            validator = UnicodeString(not_empty=True))
#        summary = forms.TextField(
#            validator = UnicodeString())
#        body = forms.TextArea(
#            rows = 15,
#            validator = UnicodeString(not_empty=True))
#        publish_date = forms.CalendarDateTimePicker(
#            validator = DateTimeConverter())
#        preview = forms.Button(
#            name='Preview',
#            attrs={'value':'Preview'})
#new_article_form = NewArticleForm('new_article_form')
#

class ChangePasswordForm(forms.TableForm):
    class fields(WidgetsList):
        password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        confirm_password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        _authentication_token = SecureToken()
changepass_validator = FilteringSchema(
    chained_validators=[FieldsMatch('password', 'confirm_password')])
change_password_form = ChangePasswordForm('change_password_form', validator=changepass_validator)


class ForgotPasswordForm(forms.TableForm):
    class fields(WidgetsList):
        email_address = forms.TextField(
            label_text = 'Email',
            validator = ExistingEmail(not_empty=True))
        _authentication_token = SecureToken()
forgot_password_form = ForgotPasswordForm('forgot_password_form')


class LoginForm(forms.TableForm):
    class fields(WidgetsList):
        email_address = forms.TextField(
            validator = Email(not_empty=True))
        password = forms.PasswordField(
            validator = UnicodeString(not_empty=True))
        _authentication_token = SecureToken()
login_validator = FilteringSchema(
    chained_validators=[ValidLogin(email='email_address', password='password')])
login_form = LoginForm('login_form', validator=login_validator)

class OpenIDLogin(forms.TableForm):
    class fields(WidgetsList):
        openid_identifier = forms.TextField(
            label_text="OpenID Identifier",
            validator = UnicodeString(not_empty=True))
        _authentication_token = SecureToken()
openid_login_form = OpenIDLogin('openid_login_form')


class OpenIDRegistrationForm(forms.TableForm):
    class fields(WidgetsList):
        displayname = forms.TextField(
            label_text = "Display Name",
            help_text = "Name that will appear when posting/commenting",
            validator = All(UnicodeString(not_empty=True), UniqueDisplayname()))
        email_address = forms.TextField(
            validator = All(Email(not_empty=True), UniqueEmail()))
        timezone = forms.SingleSelectField(
            options = pytz.common_timezones,
            validator = OneOf(pytz.common_timezones, not_empty=True))
openid_registration_form = OpenIDRegistrationForm('openid_registration_form')


class RegistrationForm(forms.TableForm):
    class fields(WidgetsList):
        displayname = forms.TextField(
            label_text = "Display Name",
            help_text = "Name that will appear when posting/commenting",
            validator = All(UnicodeString(not_empty=True), UniqueDisplayname()))
        email_address = forms.TextField(
            validator = All(Email(not_empty=True), UniqueEmail()))
        timezone = forms.SingleSelectField(
            options = pytz.common_timezones,
            validator = OneOf(pytz.common_timezones, not_empty=True))
        password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        confirm_password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        _authentication_token = SecureToken()
registration_validator = FilteringSchema(
    chained_validators=[FieldsMatch('password', 'confirm_password')])
registration_form = RegistrationForm('registration_form', validator=registration_validator)


