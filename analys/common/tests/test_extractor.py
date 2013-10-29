import unittest
from os.path import dirname, abspath

class TestExtractor(unittest.TestCase):
    def test_rar_file(self):
        from analys.common.extractor import Extractor
        from analys.plugins.interfaces import File

        with(open(dirname(abspath(__file__)) + '/samples/sample1.rar', 'rb')) as w:
            f = File('sample1.rar', w.read())
            extractor = Extractor()
        
            extractor.rar_file(f)
            self.assertEqual(1, len(extractor.samples))

    def test_rar_file_deep(self):
        from analys.common.extractor import Extractor
        from analys.plugins.interfaces import File
        from analys.exceptions import MaxFileDepth

        with(open(dirname(abspath(__file__)) + '/samples/sample6.rar', 'rb')) as w:
            f = File('sample6.rar', w.read())
            extractor = Extractor()
        
            with self.assertRaises(MaxFileDepth):
                extractor.extract(f)
    
    def test_rar_file_with_password(self):
        from analys.common.extractor import Extractor
        from analys.plugins.interfaces import File
        from analys.exceptions import NoValidPasswordFound

        with(open(dirname(abspath(__file__)) + '/samples/sample_password_infected.rar', 'rb')) as w:
            f = File('sample_password_infected.rar', w.read())
            extractor = Extractor()
        
            with self.assertRaises(NoValidPasswordFound):
                extractor.extract(f, ['test'])

    def test_zip_file(self):
        from analys.common.extractor import Extractor
        from analys.plugins.interfaces import File

        with(open(dirname(abspath(__file__)) + '/samples/sample1.zip', 'rb')) as w:
            f = File('sample1.zip', w.read())
            extractor = Extractor()
        
            extractor.zip_file(f)
            self.assertEqual(1, len(extractor.samples))

    def test_zip_file_deep(self):
        from analys.common.extractor import Extractor
        from analys.plugins.interfaces import File
        from analys.exceptions import MaxFileDepth

        with(open(dirname(abspath(__file__)) + '/samples/sample6.zip', 'rb')) as w:
            f = File('sample6.zip', w.read())
            extractor = Extractor()
        
            with self.assertRaises(MaxFileDepth):
                extractor.extract(f)


    def test_zip_file_with_password(self):
        from analys.common.extractor import Extractor
        from analys.plugins.interfaces import File
        from analys.exceptions import NoValidPasswordFound

        with(open(dirname(abspath(__file__)) + '/samples/sample_password_infected.zip', 'rb')) as w:
            f = File('sample_password_infected.zip', w.read())
            extractor = Extractor()
        
            with self.assertRaises(NoValidPasswordFound):
                extractor.extract(f, ['test'])

    def test_fetch_passwords(self):
        assert False


if __name__ == '__main__':
    unittest.main()
