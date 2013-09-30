from bluecoat import Bluecoat
from analys.plugins.plugin import Plugin

class AnalysPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)

    def submit(self):
        b = Bluecoat(self.get_resource().url)
        result = b.submit()
        self.insert(result)
        return True
