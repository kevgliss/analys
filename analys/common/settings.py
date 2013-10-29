"""
.. module:: settings
    :platform: Unix
    :synopsis: A helper module that interfaces with the analys settings that
    are persisted in the datastore.

.. version:: 0.1
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import logging

log = logging.getLogger(__name__)

class Settings(object):
    """ 
        Settings class representing all of the internal settings within
        Analys
    """
    def __init__(self, datastore):
        self.datastore = datastore
    
    def get_compressed_passwords(self, user):
        """
            Gets all possible compression passwords
        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                return value['compressed_passwords']

    def add_compressed_password(self, password, user):
        """
            Adds a password to a list of possible compression passwords
            
            Args:
                password (str): password to add
       
            Returns
                passwords (list): a list of updated passwords
        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                passwords = value['compressed_passwords']
                passwords.append(password)
                self.datastore.update('settings', value['_id'], {'compressed_passwords': passwords})
                return passwords        

    def remove_compressed_password(self, password, user):
        """
            Removes a password from the list of possible compressions passwords
            
            Args:
                password (str): password to remove
        
            Returns
                passwords (list): a list of updated passwords
        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                passwords = value['compressed_passwords']
                idx = passwords.index(password)
                
                del passwords[idx]
                self.datastore.update('settings', value['_id'], {'compressed_passwords': passwords})
                
                return passwords        

    def get_mimetype_mappings(self, user):
        """
            Return all of the currently active mimetype mappings
        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                return value['mimetype_mappings']

    def add_mimetype_mapping(self, mimetype, user):
        """
            Add a mimetype mapping to the current list of mappings

            Args:
                mimetype (tuple): Mapping to add

        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                mimetypes = value['mimetype_mappings']
                mimetypes.append(mimetype)
                self.datastore.update('settings', value['_id'], {'mimetype_mappings': mimetypes})
                return mimetypes

    def remove_mimetype_mapping(self, mimetype, user):
        """
            Removes a mimetype mapping from the current list of mappings
        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                mimetypes = value['mimetype_mappings']
                idx = mimetypes.index(mimetype)
                
                del mimetypes[idx]
                self.datastore.update('settings', value['_id'], {'mimetype_mappings': mimetypes})

                return mimetypes

    #NOTE these might be a better fit for the plugin manager
    def get_all_plugin_settings(self, user):
        """
            Gets settings for all currently installed plugins
        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                return value['plugins'] 

    def get_plugin_settings(self, plugin_name, user):
        """
            Gets the plugin settings for the plugin specified

            Args:
                plugin_name (str): name of plugin to retrieve

        """
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                for plugin in value['plugins']:
                    for name, default_values in plugin.items():
                        if plugin_name in name:
                            return plugin

    def set_plugin_settings(self, plugin_name, settings, user):
        """
            Update a plugins default settings

            Args:
                plugin_name (str): plugin to update
                settings (dict): new settings to set
        """
        
        #NOTE This feels super hacky
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                for idx, plugin in enumerate(value['plugins']):
                    for name, default_values in plugin.items():
                        if plugin_name in name:
                            value['plugins'][idx] = {plugin_name: settings}
                            self.datastore.update('settings', value['_id'], 
                                    {'plugins': value['plugins']})
                            return value['plugins'][idx]

    def delete_plugin_settings(self, plugin_name, user):
        """
            Restore plugin settings to their defaults

            Args:
                plugin_name (str): plugin to remove
                user (str): user to apply deletion
        """
        #NOTE This feels super hacky
        for value in self.datastore.get_all_documents('settings'):
            if user in value['user']:
                for idx, plugin in enumerate(value['plugins']):
                    for name, default_values in plugin.items():
                        if plugin_name in name:
                            del value['plugins'][idx]
                            self.datastore.update('settings', value['_id'], 
                                    {'plugins': value['plugins']})
                            return value['plugins']
