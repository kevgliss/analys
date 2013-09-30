
import unittest
from pyramid import testing


class SubmissionsCreate(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_submisson_create_file(self):
        from analys.views import Submissions





