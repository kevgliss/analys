from cuckoo import Cuckcoo
from analys.plugins.interfaces import File, URL

class AnalysPlugin(object):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)

    def submit(self):
        #remap analys priority to cuckcoo priority
        if "1" not in priority:
            if "low" in priority:
                priority = "1"
            elif "medium" in priority:
                priority = "2"
            elif "high" in priority:
                priority = "3" 
        
        if isinstance(self.resource, File):
            g = Cuckoo(self.hostname, self.resource.create_temp_file(),
                                "%s.%s" % (self.resource.md5(),
                                self.resource.extension(),), priority)

            g.create()
            self.resource.delete_temp_file()

        elif isinstance(self.resource, URL):
            g = Cuckoo(self.hostname, self.resource.url(), priority)
            g.create()

        results = g.report()
        
        resource_id = self.insert(result)
        #self.emit(task)

        
        
