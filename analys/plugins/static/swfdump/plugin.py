import swfdump
from analys.plugins.plugin import Plugin

class AnalysPlugin(Plugin):

    def submit(self):
        swf = swfdump.SWFDump(self.get_resource().create_temp_file())
        return swf

    def render(self):
        pass


