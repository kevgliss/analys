from gfi import GFI
from analys.plugins.interfaces import File, URL

class AnalysPlugin(object):
    def __init__(self, *args, **kwargs):
        self.resource = kwargs['resource']
        self.config = kwargs['config']

    def submit(self):
        if isinstance(self.resource, File):
            g = GFI(self.resource.create_temp_file(),
                    self.config['host'],
                    "%s.%s" % (self.resource.md5(),
                                self.resource.extension(),))

            g.submit()
            self.resource.delete_temp_file()

        elif isinstance(self.resource, URL):
            g = GFI(self.resource.url(), self.config['host'])
            g.submit()

        result = g.results()
        return result
