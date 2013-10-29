import unittest
from os.path import dirname, abspath

class TestMime(unittest.TestCase):
    def test_get_file_type(self):
        from analys.common import mime
        assert False
    
    def test_search_exe(self):
        from analys.common import mime
        from analys.plugins.interfaces import File
        with open(dirname(abspath(__file__)) + '/samples/sample1.exe', 'rb') as w:
            f = File('sample1.exe', w.read())
            self.assertEqual(mime.search(f), ('application/x-dosexec', 'exe'))

    def test_search_zip(self):
        from analys.common import mime
        from analys.plugins.interfaces import File
        with(open(dirname(abspath(__file__)) + '/samples/sample1.zip', 'rb')) as w:
            f = File('sample1.zip', w.read())
            self.assertEqual(mime.search(f), ('application/zip', 'zip'))

    def test_search_jar(self):
        from analys.common import mime
        from analys.plugins.interfaces import File
        with(open(dirname(abspath(__file__)) + '/samples/sample1.jar', 'rb')) as w:
            f = File('sample1.jar', w.read())
            self.assertEqual(mime.search(f), ('application/zip', 'jar'))

    def test_search_apk(self):
        from analys.common import mime
        from analys.plugins.interfaces import File
        with(open(dirname(abspath(__file__)) + '/samples/sample1.apk', 'rb')) as w:
            f = File('sample1.apk', w.read())
            self.assertEqual(mime.search(f), ('application/zip', 'apk'))

    def test_mime_not_found_exception(self):
        from analys.common import mime
        from analys.plugins.interfaces import File
        from analys.exceptions import InvalidMimeType
        with(open(dirname(abspath(__file__)) + '/samples/sample1.gif', 'rb')) as w:
            f = File('sample1.gif', w.read())
        
            with self.assertRaises(InvalidMimeType):
                mime.search(f)

if __name__ == '__main__':
    unittest.main()
