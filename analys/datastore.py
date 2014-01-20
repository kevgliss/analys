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

from analys.exceptions import ResourceNotFound, InvalidResourceType

log = logging.getLogger(__name__)

class Datastore(object):
    """
        This is a class that is used to connect to a MongoDB datastore
    """
    
    def __init__(self, host, port):
        """ 
            Initializes a Datastore object

            Args:
                host (str): Host to connect to
                port (str): Port to connect to

        """
        self.host = host
        self.port = int(port)

    def connect(self):
        """ 
            Creates a connection to either a singular mongodb instance or a 
            mongodb replica set.
            
            Returns:
                conn (obj): A pymongo connection Object

        """
        if '#' in self.host:
            host_parts = self.host.split('#')
            conn = MongoReplicaSetClient(host_parts[0],
                    replicaSet=host_parts[1])
        else:
            conn = Connection(self.host, self.port)

        return conn


    def store_file_data(self, data):
        """ 
            Return file_id 
        
            Args:
                data (str): A byte stream of data representing a file

            Returns:
                _id (ObjectId): A pymongo objectid representing the file
        """
        conn = self.connect()
        return gridfs.GridFS(conn.files).put(data)

    def get_file_data(self, file_id):
        """ 
            Return data from stored file

            Args:
                file_id (str): A string representing a file

            Returns:
                data (str): A byte stream of data representing a file

        """
        conn = self.connect()
        return gridfs.GridFS(conn.files).get(ObjectId(file_id)).read()

    #TODO implement pagination
    def get_all_documents(self, collection, start=None, stop=None):
        """
            Return a dict containing all documents in a collection

            WARNING: This could be a very large amount of data depending
            on the size of your database. Consider using some pagination
            to lessen the load.

            Args:
                collection (str): A string with which collection to use
                start (int): Starting entry
                stop (int): Ending entry

            Returns:
                doc (dict): A dictionary containing query results

        """
        conn = self.connect()
        c = Collection(conn.analys, collection)
        return c.find().sort("_id", -1)
    
    def get_document_by_id(self, collection, document_id):
        """
            Return a dict containing the document specified by the document_id

            Args:
                collection (str): A string with which collection to use
                document_id (str): Id representing a given document

            Returns:
                doc (dict): A dictionary containing query results

        """
        conn = self.connect()
        c = Collection(conn.analys, collection)
        return c.find_one({"_id": ObjectId(document_id)})
   
#    def delete_document_by_id(self, collection, document_id):
#        """
#            Return a dict containing the document specified by the document_id
#
#            Args:
#                collection (str): A string with which collection to use
#                document_id (str): Id representing a given document
#
#            Returns:
#                doc (dict): A dictionary containing query results
#
#        """
#        conn = self.connect()
#        c = Collection(conn.analys, collection)
#        result = c.remove({"_id": ObjectId(document_id)}, w=1)
#        
#        if result['err']:
#            return {'document_id': document_id, 'delete': False}
#        else:
#            return {'document_id': document_id, 'delete': True}

    def get_task_document(self, document_id):
        """
            Return a dict containing the document specified by the document_id

            Args:
                document_id (str): Id representing a given document

            Returns:
                doc (dict): A dictionary containing query results

        """
        task_doc = self.get_document_by_id('tasks', document_id)
        conn = self.connect()
        c = Collection(conn.analys, task_doc['plugin'])
        return c.find_one({"submission_id": task_doc['submission_id']})

    # TODO ensure that data is ok for insertion
    def ensure_safe_for_insertion(self, data):
        """ 
            Will safely commit a serizable data to the datastore. It will 
            ensure that any conditions of the datastore are met. In
            MongoDB's case this means that keys do not contain the characters 
            '$' or '.' and that the document is not greater than 16mb in size.
            It also means all strings are UTF-8 encodeable. If either of the 
            conditions are met the function will issue a warning and take 
            necessary steps to make the data safe to store.

        """
        return data

    def insert(self, collection, data):
        """
            Return a resouce_id for the successful insertion 

            Args:
                collection (str): The collection to insert data into
                data (dict): Data to insert

            Returns:
                resource_id (str): Id of created document

        """
        conn = self.connect()
        c = Collection(conn.analys, collection)
        resource_id = c.insert(self.ensure_safe_for_insertion(data))
        conn.close()
        return resource_id

    def update(self, collection, resource_id, data, upsert=False):
        """
            Return a resouce_id for the successful insertion 

            Args:
                collection (str): The collection to insert data into
                resource_id (str): Document to update
                data (dict): Data to update

            Returns:
                resource_id (str): Id of updated document

        """
        conn = self.connect()
        c = Collection(conn.analys, collection)
        c.update({"_id": ObjectId(resource_id)}, self.ensure_safe_for_insertion(data), upsert=upsert)
        conn.close()
        return resource_id

    def delete(self, collection, resource_id):
        """
            Remove an item from a collection

            Args:
                collection (str): The collection to remove data from
                resource_id (str): Document to remove

        """
        conn = self.connect()
        c = Collection(conn.analys, collection)
        c.remove(resource_id, safe=True)



