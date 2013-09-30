import unittest

class TestBluecoat(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_submit(self):
        from bluecoat import Bluecoat
        b = Bluecoat("www.google.com")
        result = b.submit()
        self.assertEquals(result, "Search Engines/Portals")

if __name__ == '__main__':
    unittest.main()
