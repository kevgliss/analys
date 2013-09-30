import unittest

class TestMime(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search_exe(self):
        from analys.utils import mime
        from analys.plugins.interfaces import File
        with open('samples/sample1.exe', 'rb') as w:
            f = File('sample1.exe', w.read())
            self.assertEqual(mime.search(f), ('application/x-dosexec', 'exe'))

    def test_search_zip(self):
        from analys.utils import mime
        from analys.plugins.interfaces import File
        with(open('samples/sample1.zip', 'rb')) as w:
            f = File('sample1.zip', w.read())
            self.assertEqual(mime.search(f), ('application/zip', 'zip'))

    def test_search_jar(self):
        from analys.utils import mime
        from analys.plugins.interfaces import File
        with(open('samples/sample1.jar', 'rb')) as w:
            f = File('sample1.jar', w.read())
            self.assertEqual(mime.search(f), ('application/zip', 'jar'))

    def test_search_apk(self):
        from analys.utils import mime
        from analys.plugins.interfaces import File
        with(open('samples/sample1.apk', 'rb')) as w:
            f = File('sample1.apk', w.read())
            self.assertEqual(mime.search(f), ('application/zip', 'apk'))

if __name__ == '__main__':
    unittest.main()
