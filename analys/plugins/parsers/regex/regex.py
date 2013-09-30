"""
.. module:: regex
    :platform: Unix
    :synopsis: Simple module that allows a user to use regex to exract IOCs from
    analys results.
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
.. version:: 1.0

"""
import re
import logging

log = logging.getLogger(__file__)

class Regex(Parser):
    def __init__(self, regex):
        """ Regex init function

        :param url: regex
        :type url: str
        """
        self.regex = regex

    def parse(value, **kwargs):
        return re.match(self.regex, value)
