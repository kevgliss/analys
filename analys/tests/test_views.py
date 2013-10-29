import unittest

from pyramid import testing
from webtest import TestApp

from conrice.tests.support import TestCase, CatchErrors

class TestApp(unittest.TestCase):
    def test_get(self):
        # app = App(request)
        # self.assertEqual(expected, app.get())
        assert False # TODO: implement your test here

class TestWorkflow(unittest.TestCase):
    def test_collection_get(self):
        # workflow = Workflow(request)
        # self.assertEqual(expected, workflow.collection_get())
        assert False # TODO: implement your test here

    def test_collection_post(self):
        # workflow = Workflow(request)
        # self.assertEqual(expected, workflow.collection_post())
        assert False # TODO: implement your test here

    def test_delete(self):
        # workflow = Workflow(request)
        # self.assertEqual(expected, workflow.delete())
        assert False # TODO: implement your test here

    def test_get(self):
        # workflow = Workflow(request)
        # self.assertEqual(expected, workflow.get())
        assert False # TODO: implement your test here

class TestSubmissions(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include("analys")
        self.config.scan("analys.views")
        self.app = TestApp(CatchErrors(self.config.make_wsgi_app()))

    def tearDown(self):
        testing.tearDown() 

    def test_collection_get(self):
        app = TestApp(main({}))
        
        app.get('/1/submissions', status=200)
        # submissions = Submissions(request)
        # self.assertEqual(expected, submissions.collection_get())
        assert False # TODO: implement your test here

    def test_collection_post(self):
        # submissions = Submissions(request)
        # self.assertEqual(expected, submissions.collection_post())
        assert False # TODO: implement your test here

    def test_delete(self):
        # submissions = Submissions(request)
        # self.assertEqual(expected, submissions.delete())
        assert False # TODO: implement your test here

    def test_get(self):
        # submissions = Submissions(request)
        # self.assertEqual(expected, submissions.get())
        assert False # TODO: implement your test here

class TestResults(unittest.TestCase):
    def test_get(self):
        # results = Results(request)
        # self.assertEqual(expected, results.get())
        assert False # TODO: implement your test here

class TestTasks(unittest.TestCase):
    def test_collection_post(self):
        # tasks = Tasks(request)
        # self.assertEqual(expected, tasks.collection_post())
        assert False # TODO: implement your test here

    def test_delete(self):
        # tasks = Tasks(request)
        # self.assertEqual(expected, tasks.delete())
        assert False # TODO: implement your test here

    def test_get(self):
        # tasks = Tasks(request)
        # self.assertEqual(expected, tasks.get())
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
