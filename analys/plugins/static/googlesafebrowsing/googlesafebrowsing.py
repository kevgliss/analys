"""
.. module:: gsafebrowsing
    :platform: Unix
    :synopsis: A module that interacts with the Google Safebrowsing api.

    Providing external information about urls for phishing detection.

    Response Objects:
    A JSON blob is returned with the information

    HTTP Response
        | 200: The queried URL is either phishing, malware or both, see the response body for the specific type.
        | 204: The requested URL is legitimate, no response body returned.
        | 400: Bad Request - The HTTP request was not correctly formed.
        | 401: Not Authorized - The apikey is not authorized
        | 503: Service Unavailable - The server cannot handle the request.

    Not all the required CGI parameters are specified
    Some of the CGI parameters are empty
    The queried URL is not a valid URL or not properly encoded

.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""

import requests
import logging

log = logging.getLogger(__file__)

class GoogleSafeBrowsing(object):
    """
    :param url: url
    :type url: str

    An example of using this class is:

        >>> g = GoogleSafeBrowsing("suspected.phishing.site.com", 'api_key')
        >>> g.submit()
    """
    def __init__(self, url, api_key):
        self.api_url = "https://sb-ssl.google.com/safebrowsing/api/lookup"
        self.parameters = {"url": url,
                  "client": 'api',
                  "appver": '1.0',
                  "pver": '3.0',
                  "apikey": api_key}

    def submit(self):
        result = "error"
        try:
            response = requests.get(self.api_url, params=self.parameters)
            if response.status_code == 204:
                result = "clean"
            if response.status_code == 200:
                result =  response.content
        except:
            self.log.error("Google Safebrowsing Exception", exc_info=True)
        return result
