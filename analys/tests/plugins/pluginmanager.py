import unittest

class TestPluginManager(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_load(self):
        pass


    def test_url_plugins(self):
        pass

    def test_file_plugins(self):

        from analys.plugins.interfaces import File
        from analys.plugins.pluginmanager import PluginManager
        from rq import Connection, Queue
        from redis import Redis
        import time
        # Tell RQ what Redis connection to use
        redis_conn = Redis()
        q = Queue(connection=redis_conn, async=False)  # no args implies the default queue


        pm = PluginManager()
        pm.load_plugins(['static'])
        with open('samples/sample1.exe', 'rb') as w:
            f = File('sample1.exe', w.read())

        for plugin, config in pm.get_plugins():
            datatypes = config['Core']['datatype'].split(',')
            if 'File' in datatypes:
                mime, ext = f.extension()
                options = {'get': True}
                valid_extensions = config['Core']['extensions'].split(',')
                if 'all' in valid_extensions  or ext in valid_extensions:
                    job = q.enqueue(plugin.AnalysPlugin(resource=f,
                            config=config, options=options).submit())

                    print job.result
                    time.sleep(2)
                    print job.result


if __name__ == '__main__':
    unittest.main()
