import unittest
from mock import MagicMock


class TestSettings(unittest.TestCase):
    def setUp(self):
        from analys.datastore import Datastore
        test_user = {
                        'user': 'test',
                        'compressed_passwords': ['infected'],
                        'mimetype_mappings': [('test1', 'test2')],
                        'plugins': [{'plugin1': 'settings'}]
                    }

        datastore = Datastore('127.0.0.1', 27017)
        self.resource_id = datastore.insert('settings', test_user)

    def tearDown(self):
        from analys.datastore import Datastore
        datastore = Datastore('127.0.0.1', 27017)
        datastore.delete('settings', self.resource_id) 

    def test_get_compressed_passwords(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.get_compressed_passwords('test')
        self.assertEquals([u'infected'], result)
        
    def test_add_compressed_password(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)
        
        s = Settings(datastore) 
        
        result = s.add_compressed_password('test', 'test')
        
        self.assertEquals(['infected', 'test'], result)

    def test_remove_compressed_password(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)
        
        s = Settings(datastore) 
        
        result = s.remove_compressed_password('infected', 'test')
        
        self.assertEquals([], result)

    def test_get_mime_type_mappings(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.get_mimetype_mappings('test')
        self.assertEquals([['test1', 'test2']], result)

    def test_add_mimetype_mapping(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.add_mimetype_mapping(['test3', 'test4'],'test')
        self.assertEquals([['test1', 'test2'], ['test3','test4']], result)

    def test_remove_mimetype_mapping(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.remove_mimetype_mapping(['test1', 'test2'],'test')
        self.assertEquals([], result)

    def test_get_all_plugin_settings(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.get_all_plugin_settings('test')
        self.assertEquals([{'plugin1': 'settings'}], result)

    def test_get_plugin_settings(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.get_plugin_settings('plugin1', 'test')
        self.assertEquals({'plugin1': 'settings'}, result)

    def test_set_plugin_settings(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.set_plugin_settings('plugin1', {'some': 'settings'}, 'test')
        self.assertEquals({'plugin1': {'some': 'settings'}}, result)
    
    def test_delete_plugin_settings(self):
        from analys.datastore import Datastore
        from analys.common.settings import Settings
        
        datastore = Datastore('127.0.0.1', 27017)

        s = Settings(datastore) 
        
        result = s.delete_plugin_settings('plugin1', 'test')
        self.assertEquals([], result)
        
if __name__ == '__main__':
    unittest.main()
