import unittest

class TestCoffeSnakePlugin(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_submit(self):
        from coffeesnake_plugin import AnalysPlugin
        ap = AnalysPlugin(data=open('sample1.jar', 'rb').read())
        print ap.submit()
