import unittest

class TestPluginManager(unittest.TestCase):
    def test_load_plugins(self):
        from analys.plugins.pluginmanager import PluginManager
        
        p = PluginManager()
        p.load_plugins(['static'])

        self.assertEqual(8, len(p.get_plugins()))

if __name__ == '__main__':
    unittest.main()
