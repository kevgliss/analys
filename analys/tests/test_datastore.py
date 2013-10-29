import unittest
from mock import MagicMock
class TestDatastore(unittest.TestCase):
    def test_ensure_safe_for_insertion(self):
        # datastore = Datastore(host, port)
        # self.assertEqual(expected, datastore.ensure_safe_for_insertion())
        assert False # TODO: implement your test here

    def test_hydrate_url(self):
        from analys.datastore import Datastore
        datastore = Datastore('127.0.0.1', 8000)
        
        submission = {
                        "resource_type": "URL", 
                        "resource": "http://example.com"
                     }

        datastore.get_document_by_id = MagicMock(return_value=submission)
        self.assertEqual(datastore.hydrate('1234', 'submissions').url, 'http://example.com')
    
    def test_hydrate_file(self):
        from analys.datastore import Datastore
        datastore = Datastore('127.0.0.1', 8000)

        submission = {
                        "resource_type": "FILE",
                        "resource": "bad.exe",
                        "file_id": "1"
                     }
        
        datastore.get_document_by_id = MagicMock(return_value=submission)
        datastore.get_file_data = MagicMock(return_value="data")
        self.assertEqual(datastore.hydrate('1234', 'submissions').data, "data")


    def test_hydrate_invalid_resource(self):
        from analys.datastore import Datastore
        from analys.exceptions import InvalidResourceType
        datastore = Datastore('127.0.0.1', 8000)

        submission = {
                        "resource_type": "random",
                        "resource": "bad.exe",
                        "file_id": "1"
                     }
        
        datastore.get_document_by_id = MagicMock(return_value=submission)

        with self.assertRaises(InvalidResourceType):
            datastore.hydrate('1234', 'submissions')


    def test_hydrate_resource_not_found(self):
        from analys.datastore import Datastore
        from analys.exceptions import ResourceNotFound
        datastore = Datastore('127.0.0.1', 8000)

        submission = {
                        "resource_type": "random",
                        "resource": "bad.exe",
                        "file_id": "1"
                     }
        
        datastore.get_document_by_id = MagicMock(return_value=None)

        with self.assertRaises(ResourceNotFound):
            datastore.hydrate('1234', 'submissions')

if __name__ == '__main__':
    unittest.main()
