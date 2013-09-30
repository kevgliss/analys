"""
.. module:: swfdump
    :platform: Unix
    :synopsis: A module used for parsing the output of the swfdump utitlity
.. moduleauthor:: Shelby Shum <shelby.shum@gmail.com>

"""

import subprocess

class SWFDump(object):
    def __init__(self, swf_file):
        self.swf_file   = swf_file

    def analyze(self):
        """
            Runs swfdump on the filepath usin the '-D' option
            -D: full version
        """
        dump = subprocess.check_output(["swfdump",self.swf_file, '-D'])
        return dump
