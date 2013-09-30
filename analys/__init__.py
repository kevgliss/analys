"""Main entry point
"""
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.renderers import JSON

from analys.datastore import Datastore
from bson import json_util
from redis import Redis

def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include("cornice")
    config.scan("analys.views")
    config.add_static_view(name='static', path='./static')

    ds = Datastore(settings['datastore.host'], settings['datastore.port'])
    config.registry.settings['datastore'] = ds
    redis = Redis(settings['message_queue.host'], int(settings['message_queue.port']))
    config.registry.settings['message_queue'] = redis

    config.add_renderer('mongo_json', json_util)

    def add_datastore(event):
        settings = event.request.registry.settings
        datastore = settings['datastore']
        event.request.datastore = datastore

    def add_message_queue(event):
        settings = event.request.registry.settings
        message_queue = settings['message_queue']
        event.request.message_queue = message_queue

    config.add_subscriber(add_message_queue, NewRequest)
    config.add_subscriber(add_datastore, NewRequest)

    return config.make_wsgi_app()
