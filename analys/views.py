"""
.. module: views
    :platform: Unix
    :synopsis: This module is responsible for defining the
    analys RESTful API.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>

"""
import sys
import logging
from pyramid.response import FileResponse
from cornice.resource import resource, view
from bson.json_util import loads, dumps

from analys import tasks
from analys import datastore
from analys.common import utils
from analys.create import url_submission, file_submission

log = logging.getLogger(__name__)

#TODO figure out how the create renderer for mongo_json data
@resource(path='/')
class App(object):
    def __init__(self, request):
        self.request = request

    def get(self):
        response = FileResponse(
                '/Users/kglisson/Documents/Code/Python/analysenv/Analys/analys/templates/index.html',
                request=self.request,
                )
        return response

@resource(collection_path='/1/workflow', path='/1/workflow/{id}', renderer='string')
class Workflow(object):
    """ Defines the 'workflow' api endpoing """
    
    def __init__(self, request):
        self.request = request

    def collection_get(self):
        """ Retrieves all workflow documents """
        return dumps(self.request.datastore.get_all_documents('workflows'))

    def get(self):
        """ Retrieves specified workflow """
        workflow_id = self.request.matchdict['id']
        return dumps(self.request.datastore.get_documnet_by_id('workflows', workflow_id))

    def collection_post(self):
        """ Creates a new workflow """
        pass
        #body = loads(self.request.body)


    def delete(self):
        """ Deletes a workflow """
        pass


@resource(collection_path='/1/submissions', path='/1/submissions/{id}', renderer="string")
class Submissions(object):
    """ Defines the 'submissions' api endpoint """

    def __init__(self, request):
        self.request = request

    #TODO figure out of how to correctly handle xsrf tokens
    def collection_post(self):
        """ Creates a new file or url submission """
        if hasattr(self.request.POST['resource'], 'filename'):
            return dumps(file_submission(self.request.POST, self.request.datastore))
        else:  
            return dumps(url_submission(self.request.POST, self.request.datastore))

        
        self.request.response.status = 403 
        return dumps({'type':'error',
                'value': """analys was unable to create a new submission, unable to identify resource type"""})

    def collection_get(self):
        """Retrieves all submission documents"""
        return dumps(self.request.datastore.get_all_documents('submissions'))

    def get(self):
        """Retrieves all related metadata for a submission"""
        submission_id = self.request.matchdict['id']
        return dumps(self.request.datastore.get_document_by_id('submissions', submission_id))
        
    def delete(self):
        """ Deletes a file or url submission """
        submission_id = self.request.matchdict['id']
        print(self.request.datastore.delete_document_by_id('submissions', submission_id))


@resource(path='/1/results/{result_type}/{result_id}', renderer='string')
class Results(object):
    """ Defines the 'results' api endpoint """
    def __init__(self, request):
        self.request = request

    def get(self):
        result_id = self.request.matchdict['result_id']
        result_type = self.request.matchdict['result_type']
        return dumps(self.request.datastore.get_document_by_id(result_type, result_id))


@resource(collection_path='/1/tasks', path='/1/tasks/{task_id}', renderer='string')
class Tasks(object):
    """ Defines the 'tasks' api endpoint """
    def __init__(self, request):
        self.request = request

    def collection_post(self):
        """ Creates a new task """
        task = self.request.json_body
        submission_id = task.get('submission_id')
        #TODO impliment priority handling
        if submission_id:
            created_tasks = tasks.create_async_tasks(self.request.datastore, task, self.request.message_queue)
            if len(created_tasks) > 0:

                success_msg = "{} Tasks successfully created for {}".format(len(created_tasks), task.get('resource')) 
                return dumps({'type': 'success',
                              'value' : success_msg})
            else:
                self.request.response.status = 500 
                return dumps({'type': 'error', 'value' : "There was an issue with your request, no tasks could be created for {}".format(task.get('resource'))})

        self.request.response.status = 403 
        return dumps({'type': 'error', 'value': 'Submissionid not found'})

    def get(self):
        """ this endpoint will fetch the result information for
            a given id

        """
        task_id = self.request.matchdict['task_id']
        return dumps(self.request.datastore.get_task_document(task_id))


    def delete(self):
        """ Deletes a file or url submission """
        try:
            return {'delete': 'true', 'resource_id': self.request.matchdict['id']}
        except:
            return {'delete': 'false', 'resource_id': self.request.matchdict['id']}
