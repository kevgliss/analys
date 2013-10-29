import unittest
from mock import MagicMock

class MyFile(object):
    def __init__(self, filename, file_obj):
        self.filename = filename
        self.file = file_obj

class TestUrlSubmission(unittest.TestCase):
    def test_url_submission(self):
        from analys.datastore import Datastore
        from analys.create import url_submission
        from analys.plugins.pluginmanager import PluginManager

        datastore = Datastore('127.0.0.1', 8000)
        datastore.insert = MagicMock(return_value='1234')
       
        plugin_manager = PluginManager()
        plugin_manager.get_plugin_options = MagicMock(return_value={"plugins": "stuff"})
        
        request_dict = {
                            "resource": "http://www.example.com",
                            "owner": "kglisson",
                       }

        response = url_submission(request_dict, datastore, plugin_manager) 
        self.assertEquals(response, {
                                        "extension": "http",
                                        "owner": "kglisson",
                                        "resource": "http://www.example.com",
                                        "plugins": {"plugins": "stuff"},
                                        "resource_type": "URL"
                                    })

#TODO make sure that compressed files are actually tested
class TestFileSubmission(unittest.TestCase):
    def test_file_submission(self):
        from analys.datastore import Datastore
        from analys.create import file_submission
        from analys.plugins.pluginmanager import PluginManager
        from analys.common import mime

        mime.search = MagicMock(return_value=("application/exe", "exe"))
        side_effects = [("application/exe", "exe"),
                       ("application/pdf", "pdf")]

        mime.search.side_effects = side_effects

        datastore = Datastore('127.0.0.1', 8000)
        datastore.insert = MagicMock(return_value='1234')
        datastore.store_file_data = MagicMock(return_value='1234')

        plugin_manager = PluginManager()
        plugin_manager.get_plugin_options = MagicMock(return_value={"plugins": "stuff"})
       

        f = MyFile("temp", open("temp", "w+"))
        request_dict = {
                            "owner": "kglisson",
                            "resource": f,
                       }
       
        for effect in side_effects:
            response = file_submission(request_dict, datastore, plugin_manager)
            self.assertEquals(response, {
                                          "owner": "kglisson",
                                          "plugins": {"plugins": "stuff"}
                                          })
    def test_zip_submission(self):
        from analys.datastore import Datastore
        from analys.create import file_submission
        from analys.plugins.pluginmanager import PluginManager
        from analys.common import mime

        mime.search = MagicMock(return_value=("application/exe", "exe"))
        side_effects = [("application/exe", "exe"),
                       ("application/pdf", "pdf")]

        mime.search.side_effects = side_effects

        datastore = Datastore('127.0.0.1', 8000)
        datastore.insert = MagicMock(return_value='1234')
        datastore.store_file_data = MagicMock(return_value='1234')
        datastore.update = MagicMock(return_value='1234')
        
        plugin_manager = PluginManager()
        plugin_manager.get_plugin_options = MagicMock(return_value={"plugins": "stuff"})
       

        f = MyFile("temp", open("temp", "w+"))
        request_dict = {
                            "owner": "kglisson",
                            "resource": f,
                       }
       
        response = file_submission(request_dict, datastore, plugin_manager)
        self.assertEquals(response, {
                                      "owner": "kglisson",
                                      "plugins": {"plugins": "stuff"}
                                      })
    
        assert False


    def test_zip_password_submission(self):
        from analys.datastore import Datastore
        from analys.create import file_submission
        from analys.plugins.pluginmanager import PluginManager
        from analys.common import mime

        mime.search = MagicMock(return_value=("application/exe", "exe"))
        side_effects = [("application/exe", "exe"),
                       ("application/pdf", "pdf")]

        mime.search.side_effects = side_effects

        datastore = Datastore('127.0.0.1', 8000)
        datastore.insert = MagicMock(return_value='1234')
        datastore.store_file_data = MagicMock(return_value='1234')

        plugin_manager = PluginManager()
        plugin_manager.get_plugin_options = MagicMock(return_value={"plugins": "stuff"})
       

        f = MyFile("temp", open("temp", "w+"))
        request_dict = {
                            "owner": "kglisson",
                            "resource": f,
                       }
       
        for effect in side_effects:
            response = file_submission(request_dict, datastore, plugin_manager)
            self.assertEquals(response, {
                                          "owner": "kglisson",
                                          "plugins": {"plugins": "stuff"}
                                          })
        assert False
    
    def test_rar_submission(self):
        from analys.datastore import Datastore
        from analys.create import file_submission
        from analys.plugins.pluginmanager import PluginManager
        from analys.common import mime

        mime.search = MagicMock(return_value=("application/exe", "exe"))
        side_effects = [("application/exe", "exe"),
                       ("application/pdf", "pdf")]

        mime.search.side_effects = side_effects

        datastore = Datastore('127.0.0.1', 8000)
        datastore.insert = MagicMock(return_value='1234')
        datastore.store_file_data = MagicMock(return_value='1234')

        plugin_manager = PluginManager()
        plugin_manager.get_plugin_options = MagicMock(return_value={"plugins": "stuff"})
       

        f = MyFile("temp", open("temp", "w+"))
        request_dict = {
                            "owner": "kglisson",
                            "resource": f,
                       }
       
        for effect in side_effects:
            response = file_submission(request_dict, datastore, plugin_manager)
            self.assertEquals(response, {
                                          "owner": "kglisson",
                                          "plugins": {"plugins": "stuff"}
                                          })
    
        assert False
    
    def test_rar_password_submission(self):
        from analys.datastore import Datastore
        from analys.create import file_submission
        from analys.plugins.pluginmanager import PluginManager
        from analys.common import mime

        mime.search = MagicMock(return_value=("application/exe", "exe"))
        side_effects = [("application/exe", "exe"),
                       ("application/pdf", "pdf")]

        mime.search.side_effects = side_effects

        datastore = Datastore('127.0.0.1', 8000)
        datastore.insert = MagicMock(return_value='1234')
        datastore.store_file_data = MagicMock(return_value='1234')

        plugin_manager = PluginManager()
        plugin_manager.get_plugin_options = MagicMock(return_value={"plugins": "stuff"})
       

        f = MyFile("temp", open("temp", "w+"))
        request_dict = {
                            "owner": "kglisson",
                            "resource": f,
                       }
       
        for effect in side_effects:
            response = file_submission(request_dict, datastore, plugin_manager)
            self.assertEquals(response, {
                                          "owner": "kglisson",
                                          "plugins": {"plugins": "stuff"}
                                          })
        assert False
if __name__ == '__main__':
    unittest.main()
