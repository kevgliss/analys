import unittest

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.passwords = ['infected']

    def tearDown(self):
        pass


    def test_extract_zip(self):
        from analys.utils.extractor import Extractor
        from analys.plugins.interfaces import File
        with(open('samples/sample1.zip', 'rb')) as w:
            f = File('sample1.zip', w.read())
            e = Extractor(f, self.passwords)
            files = e.extract()
            self.assertEquals(vars(files[0])['name'],
                    "1203/RapidFAX_id_00003248726344356807203847320475730417047590963982374102837504356891735-4635032459875086814-56389562349.pdf.exe")

#    def test_extract_rar(self):
#        from analys.utils.extractor import Extractor
#        from analys.plugins.interfaces import File
#        with(open('samples/sample1.rar', 'rb')) as w:
#            f = File('sample1.rar', w.read())
#            e = Extractor(f)
if __name__ == '__main__':
    unittest.main()
