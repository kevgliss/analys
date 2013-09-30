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

log = logging.getLogger(__file__)

class PluginManager(object):
    """
    Mount point for plugins which refer to actions that can be performed.
    Plugins implementing this reference should provide the following attributes:

    """

    def __init__(self, *args, **kwargs):
        self.plugins = []

    def get_plugins(self, *args, **kwargs):
        """ Returns a list of currently loaded plugins """
        return self.plugins

    def get_plugin_info_by_name(self, name):
        """ Returns a plugin """
        print self.plugin_info
        return self.plugin_info

    def load_plugins(self, plugin_dirs):
        """ Given a file system directory this function will recursively
        load all analys plugins discovered in that directory.
        """
        base = dirname(abspath(__file__))
        for dir in plugin_dirs:
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

