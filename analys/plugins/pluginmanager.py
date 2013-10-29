"""
.. module: pluginmanager
    :platform: Unix
    :synopsis: Is a lightweight module that is reponsible for
    interacting with analys plugins

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import logging
from os import walk
from ConfigParser import ConfigParser
from os.path import dirname, abspath, join, isdir

from analys.common.settings import Settings

log = logging.getLogger(__name__)

class PluginManager(object):
    """
        Mount point for plugins which refer to actions that can be performed.
    """

    def __init__(self, *args, **kwargs):
        self.plugins = []

    def get_plugins(self):
        """ 
            Returns a list of currently loaded plugins 
        """
        return self.plugins

    def get_plugin_options(self, types, datastore, ext=None):
        """
            This function is responsible for fetching all available options that match the
            submission type and optionally the file extension
            
            Args:
                types (list): List of submission types to filter by
                datastore (obj): A datastore object so that user defined settings can 
                                 override the plugins defined defaults
            Kwargs:
                ext (str): Optional filter returned plugins by extension applicability

            Returns:
                options (dict): A dictionary of plugin options or and empty dict
        """
        options = {}
        settings = Settings(datastore)
        for plugin, config in self.get_plugins():
            if config['Core']['datatype'] in types:
                #if we have a file deal with extension matching
                if ext:
                    extensions = config['Core']['extensions'].split(',')
                    if ext not in extensions:
                        continue

                #Plugins don't have to have options
                if hasattr(plugin, 'OPTIONS'):
                    #TODO make this a per user feature
                    #if they do check for an override
                    override = settings.get_plugin_settings(config['Core']['name'])
                    if override:
                        options[config['Core']['name']] = overide
                    else:
                        options[config['Core']['name']] = plugin.OPTIONS
                else:
                    options[config['Core']['name']] = {}
                
        return options

    def load_plugins(self, plugin_dirs):
        """ 
            Given a file system directory this function will recursively
            load all analys plugins discovered in that directory.
        """
        base = dirname(abspath(__file__))
        log.debug("plugin_base {}".format(base))
        for dir in plugin_dirs:
            log.debug(dir)
            for root, subfolder, files in walk(join(base, dir)):
                # look for a config file with *.analys-plugin
                for file in files:
                    file_parts = file.split('.')

                    if len(file_parts) != 2:
                        continue

                    if 'analys-plugin' == file_parts[1]:
                        # load the config
                        config = ConfigParser()
                        config.read(join(root, file))
                        module = config.get('Core', 'module')

                        # import as plugin
                        log.debug("analys.plugins.%s.%s.plugin" % (dir,
                            module,))
                        #the blah thing is a hack
                        self.plugins.append((
                            __import__(
                                "analys.plugins.%s.%s.plugin" %
                                    (dir, module),
                                    fromlist=['blah']), config._sections,))
                    else:
                        log.warning("No config file found in {}, Plugin was not loaded.".format(subfolder))
