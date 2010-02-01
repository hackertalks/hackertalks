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
    map.connect('/', controller='frontpage', action='index')
    
    map.connect('talkindex', '/talk', controller='talk', action='index')
    map.connect('talk_search', '/talk/search', controller='talk', action='search')
    map.connect('talk', '/talk/{id}', controller='talk', action='display')
    
    map.connect('speakerindex', '/speaker', controller='speaker', action='index')
    map.connect('speaker', '/speaker/{id}', controller='speaker', action='display')
    
    map.connect('/{controller}', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
