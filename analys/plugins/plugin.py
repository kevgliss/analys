"""
.. module: plugin
    :platform: Unix
    :synopsis: Provides useful objects for plugin creation.

.. version:: 1.0
.. module:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import os
import sys
import logging
import ConfigParser

from redis import Redis
from analys import tasks
from analys.datastore import Datastore

class Plugin(object):
    """ All analys plugins will inherit this object. It provide
    functions necessary to fetch submission data as well as storing
    plugin results.
    """

    def __init__(self, *args, **kwargs):
        self.config = kwargs['config']
        self.analys_config = ConfigParser.RawConfigParser()

        try:
            self.analys_config.read(os.environ.get('ANALYS'))
        except:
            logging.error("""No ANALYS enviromental variable not set 
                                exiting...""")
            sys.exit(1)
       
        self.resource_id = kwargs['resource_id']
        self.collection = kwargs['collection']

    def get_resource(self):
        datastore = self.get_datastore()
        return datastore.hydrate(self.resource_id, self.collection)

    def get_message_queue(self):
        return Redis(self.analys_config.get('server:message_queue', 'host'),
                int(self.analys_config.get('server:message_queue', 'port')))

    def get_datastore(self):
        return Datastore(self.analys_config.get('server:datastore', 'host'),
                int(self.analys_config.get('server:datastore', 'port')))

    #TODO add ability for plugins to pass valid status or have analys do it automatically
    def insert(self, data):
        """ We leave the decision up to the plugin whether to write its
            results back to the analys datastore. There may be plugins that
            simply complete some action and does not have anything to 
            return.
        """

        datastore = self.get_datastore()
        result_id = datastore.insert(self.config['Core']['name'].lower(),
                {'submission_id': self.resource_id, 'results': data})

        
        #update the calling submission with result id and name of the task
        datastore.update("submissions", self.resource_id,
                {"$push": 
                    {"tasks":{'task_name': self.config['Core']['name'].lower(), "result_id": result_id, "status": "Completed"}}})


    def emit(self, task):
        """ Plugins are able to 'emit' or create a new task when 
            they have finished their processing. In this way asyncronous
            tasks can be chained together to create a sequential list of tasks
            along a pipeline.
        
            A typical use case for a plugin implimenting this function is if, the
            data returned by the plugin was deemed to be `raw` or data that additional
            IOCs could be extracted. 

            For example if a plugin returned the headers of a particular request, 
            those headers might have additional IOCs such as uri's or http params
            that a analyst might look for. 

            This is in contrast to a plugin that simply returns a bool in the 
            determination of malware. There are no additional IOCs to be found
            in such a result.
        
        """
        create_tasks = tasks.create_async_tasks(self.get_datastore(), task, self.get_message_queue())

    
