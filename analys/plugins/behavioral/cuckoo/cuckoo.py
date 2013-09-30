"""
.. module:: cuckoo
    :platform: Unix
    :synopsis: A module that interacts with the cuckoo Sandbox.

.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""

import sys
import requests
import logging

log = logging.getLogger(__file__)

class Cuckoo(object):
    """ Sandbox Submit a sample to GFI Sandbox and call for the results of that
        sample.

        This is a light implementation of the cuckoo API, only functions needed
        for the plugin to work have been implemented.

        Example:
            >>> import cuckoo
            >>> fileSandbox = cuckoo.Cuckoo(raw_malware_bytes)
            >>> fileSandbox.create()
            >>> fileSandbox.report()
            {'summary':{.......},'analysis':{.......}}
            >>> urlSandbox = cuckcoo.Cuckoo('www.google.com')
            >>> urlSandbox.create()
            >>> urlSandbox.report()
            {'summary':{.......},'analysis':{.......}}

    """
    def __init__(self, hostname, submission, priority="1"):
        self.submission = submission
        self.priority = priority
        self.hostname = hostname
    
    def create(self):
        if isinstance(self.submission, basestring):
            response = requests.post("http://{}/tasks/create/url".format(self.hostname), 
                    data=data)
        
        elif isinstance(self.submission, file):
            response = requests.post("http://{}/tasks/create/file".format(self.hostname), 
                    data=data)
        
        else:
            log.error("Submission is of an invalid type: {}".format(type(self.submission)))
            sys.exit(1)

        if response.status_code == 200:
            self.task_id = response.json()['task_id']

    def report(self):
        if self.task_id:
            response = requests.get("http://{}/tasks/report/{}".format(self.hostname, self.task_id))

            if response.status_code == 200:
                return response.json()
        else:
            log.error("No task_id has been set")
