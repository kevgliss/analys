"""
.. module:: phishingTank
    :platform: Unix
    :synopsis: A module that interacts with the PhishingTank api.
        Providing external information about urls for phishing
        detection.

    A module that interacts with the PhishingTank api.
    Providing external information about urls for phishing detection.

    Response Objects:
        A JSON blob is returned with the information

    HTTP Response:
        509 HTTP is returned when the consumer has reached
        their API quote given a set time period.

    .. moduleauthor:: Kevin Glisson (kevin.glisson@gmail.com)
    .. version:: 1.0
"""
import time
import requests
import json
import logging
log = logging.getLogger(__file__)

class Phishtank(object):
    def __init__(self, url, api_key):
        self.api_url = "http://checkurl.phishtank.com/checkurl/"
        if 'http://' not in url:
            url = 'http://%s' % url
        self.data = {'url': url, 'format': "json", 'app_key': api_key}

    def submit(self):
        try:
            response = requests.post(self.api_url, data=self.data)
            if response.status_code == 200:
                return json.loads(response.content)['results']['in_database']
            elif response.status_code == 504:
                self.log.warning("Phishtank: API Limit Reached")
                time.sleep(20)
                self.submit()
            else:
                raise Exception
        except:
            log.error("PhishTank: Request could not be completed")
            return

