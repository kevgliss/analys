"""
.. module: tasks
    :platform: Unix
    :synopsis: Uses redis and it's pub/sub abilities to create a
    asynchronous tasks. In analys almost every piece of analysis
    is a task that is executed asynchronously. That analysis is always
    done in the form of a plugin. All analysis code is implimented in the
    plugin itself, therefor the functions below simply create new asychronous
    tasks for each plugin.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import logging
import datastore
from rq import Queue
from analys.plugins.pluginmanager import PluginManager

log = logging.getLogger(__name__)

def create_async_tasks(datastore, task, message_queue, priority='low'):
    """ 
        This function uses the persisted submission document to create the 
        required async tasks

        Args:
            datastore (obj): Object containing datastore connection/functions
            task (dict): Dictionary containing task information
            message_queue (obj): Object containing message_queue connection/fucntions

        Kwargs:
            priority (str): Priority of task

        Returns:
            jobs (list): List of created jobs
    """
    log.debug("Creating async tasks...")
    q = Queue(connection=message_queue, async=False) # no args implies default queue
    pm = PluginManager()

    #TODO load plugin directories from config
    pm.load_plugins(['static'])

    extension = datastore.get_document_by_id('submissions', task['submission_id'])['extension']
    
    #TODO set timeouts via the plugin config
    jobs = []
    for plugin, config in pm.get_plugins():
        #ignore plugins that dont work with this resource type
        r_type = task['resource_type']
        if r_type.lower() not in config['Core']['datatype'].lower():
            log.debug("skipping... no valid datatypes for type {}".format(r_type))
            continue

        if r_type.lower() in 'file':
            valid_extensions = config['Core']['extensions'].split(',')
            if extension not in valid_extensions:
                log.debug("skipping... no valid extensions for extension {}".format(extension))
                continue

        if len(task['plugins']) == 0:
            p = plugin.AnalysPlugin(resource_id=task['submission_id'], 
                                    collection='submissions',
                                    config=config, 
                                    resource_type=r_type)

        elif config['Core']['name'] in task['plugins']:
            p = plugin.AnalysPlugin(resource_id=task['submission_id'], 
                                    config=config,
                                    options=task['plugins'][config['Core']['name']], 
                                    collection='submissions',
                                    resource_type=r_type)


        task_id = datastore.insert('tasks', {'submission_id': task['submission_id'],
                                    'plugin': config['Core']['name']})
        
        job_id = q.enqueue(p.submit).id
        jobs.append((config['Core']['name'], job_id, task_id))
        log.debug("Creating task with plugin {} and resource_type of {}".format(config['Core']['name'], r_type))
    
    return jobs
