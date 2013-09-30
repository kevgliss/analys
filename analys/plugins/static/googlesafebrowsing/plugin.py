from googlesafebrowsing import GoogleSafeBrowsing
from analys.plugins.plugin import Plugin

class AnalysPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)

    def submit(self):
        g = GoogleSafeBrowsing(self.get_resource().url,
                self.config['Core']['apikey'])
        result = g.submit().capitalize()
        self.insert(result)
