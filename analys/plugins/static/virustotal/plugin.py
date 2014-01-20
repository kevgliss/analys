"""
.. module:: virustotal_plugin
    :synopsis: An Analys plugin that uses a VirusTotal module to submit
    and fetch imformation via the VirusTotal Public API.

    More information about the module used at:
    https://github.com/Gawen/virustotal

.. moduleauthor:: Kevin Glisson (kevin.glisson@gmail.com)
.. version:: 1.0
"""

from virustotal import VirusTotal
from analys.plugins.plugin import Plugin
from analys.plugins.interfaces import File, URL

#default options that is module has
OPTIONS = {'scan': {'type': 'bool',
                    'values': [True, False],
                    'default': False},
            'get': {'type': 'bool',
                    'values': [True, False],
                    'default': True}}

class AnalysPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)
        #TODO make sure options passing works
        self.curr_options = {}# kwargs['options']
        self.config = kwargs['config']

    def submit(self):
        """ Submit will execute the analysis portion
            of this module. Data returned will be directly
            inserted into the database unless it is
            altered by the post_submit method. This data
            will be passed back to the template for this
            module when requested by the user.
        """
        if self.curr_options.get('scan'):
            return self._scan()

        return self._get()

    def render(self, data):
        """ Returns html rendered for the module data
            passed to it. It is left up to the module
            creator how to present the data as Analys
            has no opinion on how to render your data.
            if render is not implimented Analys will
            attempt to render the data itself.
        """
        pass

    def _scan(self):
        """ Returns a report object """
        v = VirusTotal(self.config['Core']['apikey'])
        if isinstance(self.get_resource(), File):
            report = v.scan(self.get_resource().create_temp_file())

        elif isinstance(self.get_resource(), URL):
            report = v.scan(self.get_resource().url)

        report.join()
        assert report.done == True

        self.insert(report)
        return True

    #TODO fix virustotal url handling
    def _get(self):
        """ Returns a report object """
        v = VirusTotal(self.config['Core']['apikey'])
        if isinstance(self.get_resource(), File):
            report = v.get(self.get_resource().md5())

        elif isinstance(self.get_resource(), URL):
            report = v.get(self.get_resource().url)

        self.insert(report)
        return True



