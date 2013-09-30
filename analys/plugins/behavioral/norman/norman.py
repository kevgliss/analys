"""
.. module:: norman
    :platform: Unix
    :synopsis: A module that interacts with the Norman Malware Analyzer -G2 sandbox

.. moduleauthor:: Shelby Shum <shelby.shum@gmail.com>
.. lasteditedby:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import os
import sys
import requests
import json
import BeautifulSoup
import time
import logging

log = logging.getLogger(__file__)

class Norman(object):
    """ Submit a sample to the Norman Sandbox and retrieve results
    """
    def __init__(self, name, submission, host):
        """ Norman init function

        :param submission: Filepath or URL
        :type submission: String

        """
        self.apiURLs = {'file': 'http://%s/rapi/samples/basic' % host,
                        'results': 'http://%s/rapi/widgets/task_report/' % host,
                        'url': 'http://%s/rapi/samples/url' % host,
                        'delete': 'http://%s/rapi/samples/resources' % host,
                        'createTask': 'http://%s/rapi/tasks' % host,
                        'task': 'http://%s/rapi/tasks/' % host,
                        'summary': 'http://%s/rapi/widgets/event_summary/' % host,
                        'resources': 'http://%s/rapi/resources/' % host,
                        }
        self.submission = submission
        self.messages = []
        self.name = name

    def file(self):
        try:
            params = {  'owner':'maap'}
            upload = { 'upload': (self.name, open(self.submission,'rb')) }
            r = requests.post(self.apiURLs['file'],data=params,files=upload)
            response = json.loads(r.content)
            resultsCount = int(response['results_count']) - 1
            self.sampleID = response['results'][resultsCount]['samples_sample_id']
            return response
        except:
            self.log.error('Unable to submit file sample to Norman Sandbox',
                        exc_info=True,
                        extra = {
                            'data':{
                                'file': self.name,
                                'submission': self.submission
                                }
                            })
            self.messages.append({"Norman Sandbox (Behavioral)":
                            {"""Failed to submit file""":{"type":'error'}}})

    def url(self):
        try:
            params = {'owner':'maap',
                'url': self.submission }
            r = requests.post(self.apiURLs['url'], data=params)
            response = json.loads(r.content)
            results_count = int(response['results_count']) - 1
            self.sampleID = response['results'][results_count]['samples_sample_id']
            return response
        except:
            self.log.error('Unable to submit url sample to Norman Sandbox',
                        exc_info=True,
                        extra = {
                            'data':{
                                'file': self.name,
                                'submission': self.submission
                                }
                            })
            self.messages.append({"Norman Sandbox (Behavioral)":
                            {"""Failed to submit URL""": {"type": "error"}}})

    def task(self):
        try:
            params = {'sample_id': str(self.sampleID),
                      'env':'ivm',
                      'tp_FILTER.SET.V1.FULL':'1'
                     }
            r = requests.post(self.apiURLs['createTask'],data=params)
            task_response = json.loads(r.content)
            results_count = int(task_response['results_count']) - 1
            self.taskID = task_response['results'][results_count]['tasks_task_id']
            return task_response
        except:
            self.log.error('Unable to retrieve results from Norman Sandbox',
                        exc_info=True,
                        extra = {
                            'data':{
                                'file': self.name,
                                'submission': self.submission
                                }
                            })
            self.messages.append({"Norman Sandbox (Behavioral)":
                        {"""Failed to retrieve task information""": {"type": "error"}}})

    def delete(self):
        pass

    def analysis(self):
        try:
            r = requests.get(self.apiURLs['results']+str(self.taskID))
            return r.content
        except:
            self.log.error('Unable to retrieve analysis results from Norman Sandbox',
                        exc_info=True,
                        extra = {
                            'data':{
                                'file': self.name,
                                'submission': self.submission
                                }
                            })
            self.messages.append({"Norman Sandbox (Behavioral)":
                        {"""Failed to retrieve analysis information""": {"type": "error"}}})


    def summary(self):
        try:
            r = requests.get(self.apiURLs['summary']+str(self.taskID))
            return r.content
        except:
            self.log.error('Unable to retrieve summary results from Norman Sandbox',
                        exc_info=True,
                        extra = {
                            'data':{
                                'file': self.name,
                                'submission': self.submission
                                }
                            })
            self.messages.append({"Norman Sandbox (Behavioral)":
                        {"""Failed to retrieve summary information""": {"type": "error"}}})

    def patterns(self):
        try:
            r = requests.get(self.apiURLs['task']+str(self.taskID)+'/patterns')
            return json.loads(r.content)
        except:
            self.messages.append({"Norman Sandbox (Behavioral)":
                        {"""Failed to retrieve summary information""": {"type": "error"}}})


    def status(self):
        try:
            r = requests.get(self.apiURLs['task']+str(self.taskID))
            return json.loads(r.content)['results'][0]['task_state_state']
        except:
            self.messages.append({"Norman Sandbox (Behavioral)":
                        {"""Failed to retrieve task status""": {"type": "error"}}})

    def get_pcap(self):
        try:
            r = requests.get(self.apiURLs['task']+str(self.taskID)+'/resources')
            resources = json.loads(r.content)
            for f in range(len(resources['results'])):
                if resources['results'][f]['resource_magic_magic'] == 'bin:pcap':
                    self.resourceID = (resources['results'][f]['task_resources_resource_id'])
            return self.apiURLs['resources']+str(self.resourceID)+'/bin'
        except:
            self.messages.append({"Norman Sandbox (Behavioral)":
                        {"""Failed to retrieve pcap URL""": {"type": "error"}}})

    def results(self):
        """
            Use BeautifulSoup to fetch the text and use the sleep function
            in the time module to wait before re-sending the request to the sandbox
        """
        a1 = 0
        results = {'summary':{},
                    'analysis':{
                                'Process/Thread Events':{},
                                'Named Object Events':{},
                                'File System Events':{},
                                'Network Events':{},
                                'Windows Registry Events':{}
                                },
                    }
        #Loop forever until the analysis and summary are available
        # this is given by requesting task and looking at task_state_state
        while not a1:
            if self.status()=='CORE_COMPLETE':
                a1=1
                soupA = BeautifulSoup.BeautifulSoup(self.analysis())
                soupB = BeautifulSoup.BeautifulSoup(self.summary())
                half_analysis=soupA.getText('\n').split('Process/Thread Events')[0].replace('&quot;', '"').replace(', ','\n\n').split('\n\n')
                for l in half_analysis:
                    if l and not l=='Task Details':
                        temp=(l.replace('\n', ' ')).split(':')
                        results['summary'][temp[0]]=''.join(temp[1:])
                    reformattedSummary = soupB.getText('\n').replace('\n\n','\n').replace(':\n',' :  ').replace('\n\n','\n').split('\n\n')
                    for i in reformattedSummary:
                        for j in results['analysis']:
                            if j in i:
                                for line in i.split('\n'):
                                    if line and j not in line:
                                        key = line.split(':')[0]
                                        value = ':'.join(line.split(':')[1:])
                                        if results['analysis'][j].has_key(key):
                                            results['analysis'][j][key].append(value)
                                        else:
                                            results['analysis'][j][key]=[value]
            results['pattern'] = self.patterns()
            for key in results['analysis']:
                for keyz in results['analysis'][key]:
                    results['analysis'][key][keyz] = list(set(results['analysis'][key][keyz]))
            #sleep
            time.sleep(10)

            results['pcap'] = self.get_pcap()
        return results
