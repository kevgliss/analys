import unittest

class TestGFI(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def submit_file(self):
        from gfi import GFI
        g = GFI()
        g.submit()
        results = g.results()

        pass

    def submit_url(self):
        from gfi import GFI
        g = GFI()
        g.submit()
        result = g.results()
        pass

    def crash(self):
        from gfi import GFI
        g = GFI()
        g.submit()
        results = g.results()

        pass

    def invalid_filetype(self):
        from gfi import GFI
        g = GFI("/path/to/file", self.host, filename="invalid.py" )
        g.submit()
        results = g.results()
        pass


if __name__ == '__main__':
    unittest.main()

