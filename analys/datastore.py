"""
.. module: datastore
    :platform: Unix
    :synopsis: This module is the interface through which analys
    communicates with MongoDB. There are several implimentation details
    that ensure that information is successfully written to the database
    in the correct structure.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import logging
import gridfs
from bson import ObjectId
from pymongo import Connection
from pymongo import MongoReplicaSetClient
from pymongo.collection import Collection
from analys.plugins.interfaces import File, URL
from analys.common import utils

log = logging.getLogger(__name__)

class ResourceNotFound(Exception):
        pass

class InvalidResourceType(Exception):
        pass

class Datastore(object):
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def connect(self):
        """ Creates a connection to either a singular mongodb
            instance or a mongodb replica set.
        """
        if '#' in self.host:
            host_parts = self.host.split('#')
            conn = MongoReplicaSetClient(host_parts[0],
                    replicaSet=host_parts[1])
        else:
            conn = Connection(self.host, self.port)

        return conn


    def store_file_data(self, data):
        """ Return file data store """
        conn = self.connect()
        return gridfs.GridFS(conn.files).put(data)

    def get_file_data(self, file_id):
        """ Returns file data store """
        conn = self.connect()
        return gridfs.GridFS(conn.files).get(ObjectId(file_id)).read()

    #TODO be able to hydrate dynamically
    def hydrate(self, resource_id, collection):
        """ Fetches the required data in order to hydrate the
            necessary objects. This function is called by all
            plugin modules and ensures that submission data is
            available to the module in object form.
        """

        # determine how to hydrate based on what we find in the submission
        # store
        result = self.get_document_by_id(collection, resource_id)
        if not result:
            raise ResourceNotFound

        if result['resource_type'].lower() in 'URL'.lower():
            resource = URL(result['resource'])
            
        elif result['resource_type'].lower() in 'FILE'.lower():
            # fetch the actual data from the file store
            data = self.get_file_data(result['file_id'])
            resource = File(result['resource'], data)
        
        elif result['resource_type'] in 'ANALYSIS':
            resource = Analysis(data)
        else:
            raise InvalidResourceType

        return resource

    #TODO implement pagination
    def get_all_documents(self, collection, start=None, stop=None):
        conn = self.connect()
        c = Collection(conn.analys, collection)
        return c.find().sort("_id", -1)
    
    def get_document_by_id(self, collection, document_id):
        conn = self.connect()
        c = Collection(conn.analys, collection)
        return c.find_one({"_id": ObjectId(document_id)})
   
    def delete_document_by_id(self, collection, document_id):
        conn = self.connect()
        c = Collection(conn.analys, collection)
        result = c.remove({"_id": ObjectId(document_id)}, w=1)
        
        if result['err']:
            return {'document_id': document_id, 'delete': False}
        else:
            return {'document_id': document_id, 'delete': True}

    def get_task_document(self, document_id):
        task_doc = self.get_document_by_id('tasks', document_id)
        conn = self.connect()
        c = Collection(conn.analys, task_doc['plugin'])
        return c.find_one({"submission_id": task_doc['submission_id']})

    # TODO ensure that data is ok for insertion
    def insert(self, collection, data):
        """ Will safely commit a serizable data
            to the datastore. It will ensure that
            any conditions of the datastore are met. In
            MongoDB's case this means that keys do not
            contain the characters '$' or '.' and that
            the document is not greater than 16mb in size.
            It also means all strings are UTF-8 encodeable.
            If either of the conditions are met the function
            will issue a warning and take necessary steps to
            make the data safe to store.

        """
        conn = self.connect()
        c = Collection(conn.analys, collection)
        resource_id = c.insert(data)
        conn.close()
        return resource_id

    # TODO ensure that data is ok for insertion
    def update(self, collection, resource_id, data):
        conn = self.connect()
        c = Collection(conn.analys, collection)
        c.update({"_id": ObjectId(resource_id)}, data)
        conn.close()
        return True



