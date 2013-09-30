from phishtank import Phishtank
from analys.plugins.plugin import Plugin

class AnalysPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)

    def submit(self):
        p = Phishtank(self.get_resource().url,
                self.config['Core']['apikey'])
        result = p.submit()
        self.insert(result)
        return True
