from analys.plugins.plugin import Plugin
from analys.plugins.parsers.regex import Regex

class AnalysPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)

    def submit(self, search_document, collection, document_id):
        r = Regex(string) 
        data = self.datastore.get_document_by_id(collection, document_id)
        
        matches = []
        while True:
            seg = self.traverse(data).next()
            if seg:
                matches += r.parse(seg)
            else:
                break
        
        resource_id = self.insert(matches) 
