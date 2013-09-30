import unittest

class TestPhishtank(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_submit(self):
        from phishtank import Phishtank
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read('phishtank.plug')
        p = Phishtank("http://bankodelpacifico.com",
                config.get('Core','APIKey'))
        result = p.submit()
        self.assertFalse(result['results']['in_database'])

if __name__ == '__main__':
    unittest.main()

