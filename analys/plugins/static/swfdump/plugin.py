import swfdump
from analys.plugins.interfaces import File

class AnalysPlugin(object):
    def __init__(self, *args, **kwargs):
        self.resource = kwargs['resource']

    def submit(self):
        swf = swfdump.SWFDump(self.resource.create_temp_file())
        return result

    def render(self):
        pass


