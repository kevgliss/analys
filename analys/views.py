"""
.. module: views
    :platform: Unix
    :synopsis: This module is responsible for defining the
    analys RESTful API.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>

"""
import os
import sys
import logging

from cornice.resource import resource, view
from pyramid.config import Configurator
from pyramid.response import FileResponse

from bson.json_util import loads, dumps

from analys import tasks
from analys import datastore
from analys.create import url_submission, file_submission

from pprint import pprint

log = logging.getLogger(__name__)

#TODO figure out how the create renderer for mongo_json data
#TODO figure out of how to correctly handle xsrf tokens
@resource(path='/')
class App(object):
    def __init__(self, request):
        self.request = request

    def get(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        response = FileResponse(
                os.path.join(cwd, 'templates', 'index.html'),
                request=self.request,
                )
        return response



@resource(collection_path='/1/submissions', path='/1/submissions/{id}', renderer="string")
class Submissions(object):
    """ Defines the 'submissions' api endpoint """

    def __init__(self, request):
        self.request = request

    def collection_post(self):
        '''
           .. http:post:: /1/submissions

           Create a new submission

           **Example request**:

           .. sourcecode:: http

              POST /1/submission HTTP/1.1
              Host: example.com
              RequestPayload:
                ------WebKitFormBoundaryyB4hB03GodaSsiQw
                Content-Disposition: form-data; name="owner"

                kglisson
                ------WebKitFormBoundaryyB4hB03GodaSsiQw
                Content-Disposition: form-data; name="resource"; filename="9d858a53196b937c1ef426cc22c1e3d8"
                Content-Type: application/octet-stream


                ------WebKitFormBoundaryyB4hB03GodaSsiQw--
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript

                {
                    "resource": "9d858a53196b937c1ef426cc22c1e3d8", 
                    "extension": "exe", 
                    "file_id": "524a50901926a7e3dac7ff52", 
                    "plugins": {
                                   "Pescanner": {}
                               }, 
                    "owner": "kglisson", 
                    "_id": {
                            "$oid": "524a50901926a7e3dac7ff57"
                           }, 
                    "resource_type": "FILE"
                }       
           
           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
           :statuscode 404: unable to find the resource type
        
        '''
        if hasattr(self.request.POST['resource'], 'filename'):
            return dumps(file_submission(self.request.POST,
                                         self.request.datastore,
                                         self.request.plugin_manager))
        else:  
            return dumps(url_submission(self.request.POST,
                                        self.request.datastore,
                                        self.request.plugin_manager))

        self.request.response.status = 404 
        return dumps({'type':'error',
                'value': """analys was unable to create a new submission, unable to identify resource type"""})

    #TODO implement pagination
    def collection_get(self):
        '''
           .. http:get:: /1/submissions

           Get all submissions

           **Example request**:

           .. sourcecode:: http

              GET /1/submission HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                [
                    {
                        "resource": "9d858a53196b937c1ef426cc22c1e3d8", 
                        "extension": "exe", 
                        "file_id": "524a50901926a7e3dac7ff52", 
                        "plugins": {
                                       "Pescanner": {}
                                   }, 
                        "owner": "kglisson", 
                        "_id": {
                                "$oid": "524a50901926a7e3dac7ff57"
                               }, 
                        "resource_type": "FILE"
                    }
                ]       
           
           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
        '''
        return dumps(self.request.datastore.get_all_documents('submissions'))

    def get(self):
        '''
           .. http:get:: /1/submissions/{id}

           Get all submissions

           **Example request**:

           .. sourcecode:: http

              GET /1/submission/524a50901926a7e3dac7ff57 HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                {
                    "resource": "9d858a53196b937c1ef426cc22c1e3d8", 
                    "extension": "exe", 
                    "file_id": "524a50901926a7e3dac7ff52", 
                    "plugins": {
                                   "Pescanner": {}
                               }, 
                    "owner": "kglisson", 
                    "_id": {
                            "$oid": "524a50901926a7e3dac7ff57"
                           }, 
                    "resource_type": "FILE"
                }
           
           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
        '''
        submission_id = self.request.matchdict['id']
        return dumps(self.request.datastore.get_document_by_id('submissions', submission_id))

    #TODO test        
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
        '''
           .. http:get:: /1/results/{results_type}/{result_id}

           Get result

           **Example request**:

           .. sourcecode:: http

              GET /1/results/pescanner/5248fdd91926a75b98c4d4a7 HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                {
                    "submission_id": "5248fdd21926a75b98c4d4a1", 
                    "_id": {"$oid": "5248fdd91926a75b98c4d4a7"}, 
                    "results": {...}
                }

           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
        '''
        
        result_id = self.request.matchdict['result_id']
        result_type = self.request.matchdict['result_type']
        return dumps(self.request.datastore.get_document_by_id(result_type, result_id))


@resource(collection_path='/1/tasks', path='/1/tasks/{task_id}', renderer='string')
class Tasks(object):
    """ Defines the 'tasks' api endpoint """
    def __init__(self, request):
        self.request = request

    def collection_post(self):
        '''
           .. http:post:: /1/tasks/{task_id}

           Create a task

           **Example request**:

           .. sourcecode:: http

              POST /1/tasks HTTP/1.1
              Host: example.com
              Request Payload: {
                                    "owner": kglisson,
                                    "plugins": {"Pescanner": {}},
                                    "resource": "bad.exe",
                                    "resource_type": "FILE",
                                    "submission_id": "524a55901926a7e59522030d"
                                }
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                {
                    "type": "success", 
                    "value": "1 Task successfully created for bad.exe
                }

           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
           :statuscode 404: submissionid not found
           :statuscode 500: tasks could not be created
        '''

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

        self.request.response.status = 404
        return dumps({'type': 'error', 'value': 'Submissionid not found'})

    def get(self):
        task_id = self.request.matchdict['task_id']
        return dumps(self.request.datastore.get_task_document(task_id))


    def delete(self):
        """ Deletes a file or url submission """
        try:
            return {'delete': 'true', 'resource_id': self.request.matchdict['id']}
        except:
            return {'delete': 'false', 'resource_id': self.request.matchdict['id']}
          

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
        return dumps(self.request.datastore.get_document_by_id('workflows', workflow_id))

    def collection_post(self):
        """ Creates a new workflow """
        pass
    
    def delete(self):
        """ Deletes a workflow """
        pass


@resource(collection_path='/1/settings/{type}', path='/1/settings/{type}/{value}', renderer='string')
class Settings(object):
    """ Defines the 'settings' api"""
    def __init__(self, request):
        self.request = request

    def collection_get(self):
        '''
           .. http:get:: /1/settings/{type}

           Get analys settings

           **Example request**:

           .. sourcecode:: http

              GET /1/settings HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                {
                }

           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
           :statuscode 404: invalid setting type
           :statuscode 404: settings not found
        '''
        setting_type = self.request.matchdict['type']
        if 'passwords' in setting_type:
            results = dumps(self.request.settings.get_compressed_passwords())
        
        elif 'plugin' in setting_type:
            results = dumps(self.request.settings.get_all_plugin_default_settings())
        
        elif 'mimetype' in setting_type:
            results = dumps(self.request.settings.get_mimetype_mappings())

        else:
            self.request.response.status = 404
            return dumps({'type': 'error', 'value': "Invalid setting type"})

        if results:
            return dumps(results)
        else:
            self.request.response.status = 404
            return dumps({'type': 'error', 'value': 'Settings {} not found'.format(setting_type)})

    
    
    def post(self):
        '''
           .. http:post:: /1/settings/{type}/{value}

           Edits a setting

           **Example request**:

           .. sourcecode:: http

              POST /1/settings/mimetype HTTP/1.1
              Host: example.com
              Request Payload: {
                                    "owner": kglisson,
                                    "plugins": {"Pescanner": {}},
                                    "resource": "bad.exe",
                                    "resource_type": "FILE",
                                    "submission_id": "524a55901926a7e59522030d"
                                }
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                {
                    "type": "success", 
                    "value": ""
                }

           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
           :statuscode 404: setting type not found
        '''
        setting_type = self.request.matchdict['type']
        if 'passwords' in setting_type:
            results = dumps(self.request.settings.get_compressed_passwords())
        
        elif 'plugin' in setting_type:
            results = dumps(self.request.settings.get_all_plugin_default_settings())
        
        elif 'mimetype' in setting_type:
            results = dumps(self.request.settings.get_mimetype_mappings())

        else:
            self.request.response.status = 404
            return dumps({'type': 'error', 'value': "invalid setting type"})


    def delete(self):
        '''
           .. http:delete:: /1/settings/{type}/{value}

           Delete a setting

           **Example request**:

           .. sourcecode:: http

              DELETE /1/tasks HTTP/1.1
              Host: example.com
              Accept: application/json, text/javascript

           **Example response**:

           .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: text/javascript
                {
                    "type": "success", 
                    "value": "setting successfully deleted
                }

           :reqheader Accept: the response content type depends on
                              :mailheader:`Accept` header
           :resheader Content-Type: this depends on :mailheader:`Accept`
                                    header of request
           :statuscode 200: no error
           :statuscode 404: setting type not found
        '''
        setting_type = self.request.matchdict['type']
        value = self.request.matchdict['value']
        if 'passwords' in setting_type:
            self.request.settings.remove_compressed_password(value)
        
        elif 'plugin' in setting_type:
            self.request.settings.get_all_plugin_default_settings(value)
        
        elif 'mimetype' in setting_type:
            self.request.settings.get_mimetype_mappings(value)

        else:
            self.request.response.status = 404
            return dumps({'type': 'error', 'value': "setting type not found"})

        return dumps({'type': 'success', 'value': 'setting successfully deleted'})
