"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    
    # CUSTOM ROUTES HERE
    map.connect('home', '/', controller='frontpage', action='index')
    
    map.connect('talkindex', '/talk', controller='talk', action='index')
    map.connect('talk_search', '/talk/search', controller='talk', action='search')
    map.connect('talk', '/talk/{id}', controller='talk', action='display')
    
    map.connect('speakerindex', '/speaker', controller='speaker', action='index')
    map.connect('speaker', '/speaker/{id}', controller='speaker', action='display')
    
    # Accounts
    map.connect('account_login', '/accounts/login', controller='accounts', action='login')
    map.connect('account_register', '/accounts/register', controller='accounts', action='register')
    map.connect('account_logout', '/accounts/logout', controller='accounts', action='logout')
    map.connect('verify_email', '/accounts/verify_email/{token}', controller='accounts', action='verify_email')
    map.connect('forgot_password', '/accounts/forgot_password', controller='accounts', action='forgot_password')
    map.connect('reset_password', '/accounts/reset_password/{token}', controller='accounts', action='change_password')
    
    # OpenID URL's
    map.connect('openid_associate', '/accounts/openid/associate', controller='accounts', action='openid_associate')
    map.connect('openid_register', '/accounts/openid/register', controller='accounts', action='openid_register')
    map.connect('openid_login', '/accounts/openid/login', controller='consumer', action='login')
    map.connect('openid_process', '/accounts/openid/process', controller='consumer', action='process')
    map.connect('openid_create', '/accounts/openid/create', controller='consumer', action='create')

    map.connect('/{controller}', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    
    return map
