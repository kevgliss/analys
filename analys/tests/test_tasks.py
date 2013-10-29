import unittest
from mock import MagicMock

class MyQueue(MagicMock):
    def __init__(self, *args, **kwargs):
        pass

    def enqueue(self, *args, **kwargs):
        return 100

class MyPlugin(MagicMock):
    def __init__(self, *args, **kwargs):
        pass

    def submit(*args, **kwargs):
        pass

class MyPluginManager(MagicMock):
    def __init__(self, *args, **kwargs):
        pass

    def load_plugins(self):
        pass

    def get_plugins(self, directory):
        return [MyPlugin()]

#TODO FIX
class TestCreateAsyncTasks(unittest.TestCase):
    def test_create_async_tasks(self):
        import rq
        rq.Queue = MyQueue
        from analys.datastore import Datastore
        from analys.plugins.pluginmanager import PluginManager
        from analys.tasks import create_async_tasks

        p = PluginManager()
        p.get_plugins = MagicMock(return_value=MyPlugin())
        
        datastore = Datastore('127.0.0.1', 8000)
        submission = {
                        "resource_type": "FILE",
                        "resource": "bad.exe",
                        "file_id": "1",
                        "extension": "exe"
                     }

        datastore.get_document_by_id = MagicMock(return_value=submission)
       
        task = {
                  "resource_type": "FILE",
                  "resource": "bad.exe",
                  "file_id": "1",
                  "extension": "exe",
                  "plugins": {},
                  'submission_id': '1234'
                }
       
        print create_async_tasks(datastore, task, 'queue')
        self.assertTrue(len(create_async_tasks(datastore, task, 'queue')) > 0)

if __name__ == '__main__':
    unittest.main()
