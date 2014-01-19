"""Main entry point
"""
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.renderers import JSON

from redis import Redis
from bson import json_util
from analys.datastore import Datastore
from analys.plugins.pluginmanager import PluginManager

def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include("cornice")
    config.scan("analys.views")
    config.add_static_view(name='static', path='./static')

    ds = Datastore(settings['datastore.host'], settings['datastore.port'])
    config.registry.settings['datastore'] = ds

    # s = Settings(ds)
    # config.registry.settings['settings'] = s
    
    redis = Redis(settings['message_queue.host'], int(settings['message_queue.port']))
    config.registry.settings['message_queue'] = redis

    p = PluginManager()
    p.load_plugins(settings['plugin_dirs'].split(','))
    config.registry.settings['plugin_manager'] = p
    
    config.add_renderer('mongo_json', json_util)

    def add_app_objects(event):
        settings = event.request.registry.settings
        event.request.datastore = settings['datastore']
        event.request.plugin_manager = settings['plugin_manager']
        event.request.message_queue = settings['message_queue']
        # event.request.settings = settings['settings']

    config.add_subscriber(add_app_objects, NewRequest)

    return config.make_wsgi_app()
