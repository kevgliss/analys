"""
.. module: create
    :platform: Unix
    :synopsis: This module will contains the methods to
    correctly create the two types of submissions that analys
    allows.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import base64
from analys.common import mime
from analys.common import utils
from analys.common.url import deobfuscate
from analys.plugins.interfaces import File
from analys.common.extractor import Extractor
from analys.plugins.pluginmanager import PluginManager

def url_submission(request_dict, datastore):
    """ responsible for fetching all available options that are currently
        installed it will then return the deobfuscated url along with options
        and modules available for analysis
    """
    response = {}

    # TODO check for existing identical resource, confirm creation
    #fetch all the options from the installed plugins
    #TODO set the plugin directorys via a config file
    p = PluginManager()
    p.load_plugins(['static'])
    
    response['extension'], response['resource'] = deobfuscate(request_dict['resource'].strip())

    response['owner'] = request_dict['owner']
    response['resource_type'] = 'URL'
    #determine resource type
    datastore.insert('submissions', response)
    
    #purposely dont store plugin options with submisison data
    response['plugins'] = get_plugin_options(p, ['URL', 'File,URL'])
    return response


def file_submission(request_dict, datastore):
    """ responsible for fetching all available options that are currently
        install, also responsible for handling the extraction of zip/rars
        into seperate submissions
    """
    response = {}

    response['owner'] = request_dict['owner']
    p = PluginManager()
    #load these on app init?
    p.load_plugins(['static'])

    f = File(request_dict['resource'].filename, request_dict['resource'].file.read())
    mimetype, extension = mime.search(f)
    #TODO create a global errors
    if not mimetype:
        return

    if extension in ['zip', 'rar']:
        #TODO set passwords via the db or passed in at runtime
        passwords = ['infected']
        for extracted_file in Extractor(f, passwords):
            mimetype, extension = mime.search(extracted_file)

            #save file off for later retrieval
            #TODO move to datastore.py and dedup files by hash
            file_id = datastore.store_file_data(extracted_file)
            response.update({'resource': request_dict['resource'].filename , 'file_id':
                str(file_id), 'resource_type': 'FILE', 'extension': extension})
            datastore.insert('submissions', response)
            response['plugins'] = get_plugin_options(p, ['File', 'File,URL'], extension)
    else:
        file_id = datastore.store_file_data(f.data)
        response.update({'resource': request_dict['resource'].filename, 'file_id':
            str(file_id), 'resource_type': 'FILE', 'extension': extension})
        datastore.insert('submissions', response)
        response['plugins'] = get_plugin_options(p, ['File', 'File,URL'], extension)

    return response 

def get_plugin_options(pluginmanager, types, ext=None):
    """ fetches all available plugins given a particular file/url """
    options = {}

    for plugin, config in pluginmanager.get_plugins():
        if config['Core']['datatype'] in types:
            #if we have a file deal with extension matching
            if ext:
                extensions = config['Core']['extensions'].split(',')
                if ext not in extensions:
                    continue

            #not all plugins have options
            try:
                options[config['Core']['name']] = plugin.OPTIONS
            except:
                options[config['Core']['name']] = {}

    return options
