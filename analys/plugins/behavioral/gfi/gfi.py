"""
.. module:: gfi
    :platform: Unix
    :synopsis: A module that interacts with the GFI Sandbox.

..moduleauthor:: Kevin Aziz <kevin.aziz@gmail.com>
"""
import time
import json
import requests
import logging
import hashlib
from datetime import datetime, timedelta

log = logging.getLogger(__file__)

class GFI(object):
    """ Sandbox Submit a sample to GFI Sandbox and call for the results of that
        sample.

        Example:
            >>> import gfi
            >>> fileSandbox = gfi.GFI('evil_executable.exe','path/to/file.malware')
            >>> fileSandbox.file()
            >>> fileSandbox.results()
            {'summary':{.......},'analysis':{.......}}
            >>> urlSandbox = gfi.GFI('url','www.google.com')
            >>> urlSandbox.url()
            >>> urlSandbox.results()
            {'summary':{.......},'analysis':{.......}}

    """
    def __init__(self, submission, host, filename=None, priority="low"):
        """ Sandbox init function

        :param filename: File name to use in the sandbox (Must end in proper extension)
        :type filename: string
        :param submission: Filepath or URL
        :type submission: string

        """
        # hash filenames, but keep extension gfi doesn't like non-ascii
        # filenames or names over 255 chars long
        if filename:
            parts = filename.split(".")
            m = hashlib.md5()
            m.update(parts[0])
            parts[0] = m.hexdigest()
            self.filename = ".".join(parts)
        else:
            self.filename = filename

        self.submission = submission
        self.priority = priority

        self.apiURLs = {
                'submit':'http://%s/api.php/submit.json/' % host,
                'summary':'http://%s/api.php/behavior.json/?sample=' % host,
                'analysis':'http://%s/api.php/xml/?analysis=' % host,
                'delete':'http://%s/api.php/delete.json/?analysis=' % host,
                'errors':'http://%s/api.php/analyses.json/?analysis=' % host,
                'sandboxes':'http://%s/api.php/sandboxes' % host,
                'revert':'http://%s/inc/ajax.php?action=revert&sbid=' % host
                }



    def submit(self):
        #Revert any sandboxes when needed
        self.manage_sandboxes()
        if self.filename:
            return self.file()
        else:
            return self.url()

    def manage_sandboxes(self):
        try:
            r = requests.get(self.apiURLs['sandboxes'])
            response = json.loads(r.content)
            for sandbox in response['sandboxes']:
                last_status_update =  datetime.strptime(
                        sandbox['sandbox']['last_status_update'],
                        '%Y-%m-%d %H:%M:%S')

                now = datetime.now()
                elapsed = now - last_status_update

                #make sure that sandbox has been dead for at least 10 min
                #before reverting
                if elapsed > timedelta(minutes=10):
                        #revert
                        r = requests.get(self.apiURLs['revert'] +
                                sandbox['sandbox']['id'])
                        if r.status_code == 200:
                            self.log.warning("VM-%s successfully reverted" %
                                    sandbox['sandbox']['id'])
                        else:
                            self.log.error("VM-%s failed to revert" %
                                    sandbox['sandbox']['id'], exc_info=True)
        except:
            self.log.error('Unable to manage_sandboxes',
                    exc_info=True)

    def file(self):
        try:
            self.file = True
            params = {
                "email":"me@localhost",
                "reanalyze":'1',
                "notes":"Analys Submission",
                "priority": self.priority
                 }

            upfile = { 'upfile': (self.filename,open(self.submission,'rb')) }
            r = requests.post(self.apiURLs['submit'],data=params,files=upfile)
            response = json.loads(r.content)
            self.sandboxID = response['submission_results'][0]['submission']['sample_id']
            return response
        except:
            self.log.error('Unable to submit file sample to GFI Sandbox',
                        exc_info=True,
                        extra = {
                            'data':{
                                 'file': self.filename,
                                 'submission': self.submission
                             }
                            })

            self.messages.append({"GFI Sandbox (Behavioral)":
                {"""Could not connect to host""": {"type": "error"}}})

    def url(self):
        try:
            self.url = True
            params = {
                "url[0]": self.submission,
                "email":"me@localhost",
                "reanalyze":1,
                "notes":"Analys Submission",
                "priority": self.priority
                }

            r = requests.post(self.apiURLs['submit'],data=params)
            response = json.loads(r.content)
            self.sandboxID = response['submission_results'][0]['submission']['sample_id']
            return response
        except:
            self.log.error('Unable to submit url sample to GFI Sandbox', exc_info=True,
                    extra = {
                        'data':{
                            'file': self.filename,
                            'submission': self.submission
                            }
                        })

            self.messages.append({"GFI Sandbox (Behavioral)":
                {"""Could not connect to host""": {"type": "error"}}})


    def summary(self):
        while(True):
            r = requests.get(self.apiURLs['summary']+str(self.sandboxID))
            response = json.loads(r.content)

            if isinstance(response, list):
                self.analysisID = response[0]['dbt_analysis_info'][-1]['analysis_id']
                r = requests.get(self.apiURLs['errors']+str(self.analysisID))
                responseError = json.loads(r.content)
                if responseError.get("analyses")[0]:
                    if responseError["analyses"][0]["analysis"]["status"].lower() == "error":

                        self.messages.append(
                            {"GFI Sandbox (Behavioral)": {
                             responseError["analyses"][0]["analysis"]["error"].title():{
                                 "type": "error"}}})
                        self.log.error(
                            "GFI Sandbox %s" %
                            responseError["analyses"][0]["analysis"]["error"],
                            extra = {
                                'data':{
                                    'file': self.filename,
                                    'submission': self.submission
                                    }
                                })
                        raise Exception("GFI experienced an issue and could not continue")

                if len(response[0]['dbt_analysis_info'][-1]['dbt']) > 0:
                    self.analysisID = response[0]['dbt_analysis_info'][-1]['analysis_id']
                    break
            #the result might not be done yet
            time.sleep(30)

        return response

    def analysis(self):
        while(True):
            r = requests.get(self.apiURLs['analysis']+str(self.analysisID))
            try:
                #figure out better way to handle this
                analysis = xmltodict.parse(r.content)
                break
            except:
                #check for errors
                #use analysisId
                r = requests.get(self.apiURLs['errors']+str(self.analysisID))
                response = json.loads(r.content)
                if response.get("analyses")[0]:
                    if response["analyses"][0]["analysis"]["status"].lower() == "error":
                        self.messages.append({"GFI Sandbox (Behavioral)":
                            {response["analyses"][0]["analysis"]["error"]:{"type": "error"}}})
                        self.log.error(
                            "GFI Sandbox %s" % response["analyses"][0]["analysis"]["error"],
                            extra = {
                                'data':{
                                    'file': self.filename,
                                    'submission': self.submission
                                    }
                                })
                        break
                time.sleep(5)
        return analysis

    def results(self):
        results = {}
        try:
            results['summary'] = self.summary()
            results['analysis'] = self.analysis()
            return results
        except:
            self.log.error("Unable to retrieve GFI results", exc_info=True, extra={
                'data':{'file': self.filename,
                'submission': self.submission}})

            self.messages.append({"GFI Sandbox (Behavioral)":
                {"""GFI Sandbox results could not be retrieved""": {"type": "error"}}})

    def delete(self):
        r = requests.get(self.apiURLs['delete']+str(self.sandboxID))
        self.delete = r.content
        return self.delete
