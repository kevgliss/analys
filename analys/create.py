"""
.. module: create
    :platform: Unix
    :synopsis: This module will contains the methods to
    correctly create the two types of submissions that analys
    allows.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
#TODO check for existing identical resource, confirm creation
import re
import logging

from analys.common import mime
from analys.common.settings import Settings
from analys.common.extractor import Extractor
from analys.plugins.interfaces import File, URL

log = logging.getLogger(__name__)

def url_submission(request_dict, datastore, plugin_manager):
    """ 
        This function is responsible for fetching all available options that are currently
        installed. It should be used used for any submission with a `resource_type` of `URL`.
        
        Args:
            request_dict (dict): The request dictionary as created by pyramid
            datastore (obj): The common datastore object used for all application
                             datastore operations.
            plugin_manager (obj): An instntiated plugin_manager that was configured on startup

        Returns:
            response (dict): A response dictionary containing the deobfuscated url and
                             all the available plugins and options found to be installed/enabled
    """
    def _obfuscate(url):
        if not url.startswith('http://'):
            url = "".join(['http://', url])
        url = re.sub('(?i)http', 'hxxp', url)
        return url


    #TODO figure out more sane what to obfuscate/deobfuscate url at anytime
    response = {}
    response['resource'] = _obfuscate(request_dict['resource'])
    response['owner'] = request_dict['owner']
    response['resource_type'] = 'URL'
    response['extension'] = '' 
    response['submission_id'] = datastore.insert('submissions', response)
    #purposely dont store plugin options with submisison data
    response['plugins'] = plugin_manager.get_plugin_options(['URL', 'File,URL'], datastore)
    return response


def file_submission(request_dict, datastore, plugin_manager):
    """
        This function is responsible for fetching all available options that are currently
        installed. It should be used for any submission with a `resource_type` of `FILE`. 
        
        Args:
            request_dict (dict): The request dictionary as created by pyramid
            datastore (obj): The common datastore object used for all application
                             datastore operations.
            plugin_manager (obj): An instntiated plugin_manager that was configured on startup

        Returns:
            response (dict): A response dictionary containing all the available plugins and 
            options found to be installed/enabled
    """
    def _submit_file(file_data, filename, parent=False):
        file_id = datastore.store_file_data(file_data)
        
        file_response = {'resource': filename,
                         'file_id': file_id, 
                         'resource_type': 'FILE', 
                         'extension': filename.split('.')[-1]} # TODO: Hack in order to remove deadlock a couple lines below
        if parent:
             file_response.update({"parent": parent})
        
        return datastore.insert('submissions', file_response)

    response = {}
    response['owner'] = request_dict['owner']
    response['resource_type'] = 'FILE'
    response['resource'] = request_dict['resource'].filename

    parent_id = _submit_file(request_dict['resource'].file.read(), request_dict['resource'].filename)
   
    response.update({'_id': parent_id})
    f = File(parent_id, 'submissions', datastore)
    
    s = Settings(datastore)
    mimetypes = s.get_mimetype_mappings()
    
    mimetype, extension = mime.search(f, mimetypes)

    #TODO create frontend for password insertion
    if extension in ['zip', 'rar']:
        e = Extractor(f.data)

        if request_dict.get('passwords'):
            files = e.extract(passwords=request_dict['passwords'])
        else: 
            files = e.extract()
        
        for extracted_file in files:
            mimetype, extension = mime.search(extracted_file)
            child_id = _submit_file(extracted_file, extracted_file.filename) 
            #update orig submission with children
            #TODO change this to a push, make sure update can handle that
            datastore.update('submissions', parent_id, {"children": child_id})
            response['plugins'] = plugin_manager.get_plugin_options(['file', 'file,url'], datastore, extension)
            
    else:
        #we dont want to try and find plugins for compressed files
        
        response['plugins'] = plugin_manager.get_plugin_options(['file', 'file,url'], extension)

    return response 

