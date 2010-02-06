<%!
    from hackertalks.model.forms import login_form, openid_login_form
%>
<div class="yui-b content">
    <h1>${_('Login')}</h1>
    ${login_form(action=url('account_login')) | n}
    <p>${h.link_to('Forgot your password?', url=url('forgot_password'))}</p>
    
    <h1>${_('Login with OpenID')}</h1>
    ${openid_login_form(action=url('openid_login')) | n}
</div>
<%def name="title()">${parent.title()} - ${_('Login')}</%def>
<%inherit file="../layout.mako" />
