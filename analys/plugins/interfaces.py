"""
.. module:: interfaces
    :platform: Unix
    :synopsis: This module is responsible holding common
    objects used throughout analys.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import os
import hashlib
import tempfile
from analys.common.mime import search as mime_search

class File(object):
    """ Plugins for this class analyze Files """
    def __init__(self, filename, data):
        self.name = filename
        self.data = data
        self.path = None

    def create_temp_file(self):
        """ Return the path of a temporary file, it will only create
            one temporary file for this object.
        """
        # if temporary has not already been created, create one
        if not self.path:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(self.data)
                self.path = f.name
                return f.name
        else:
            return self.path

    def delete_temp_file(self,):
        """ Tries to delete a temporary file """
        if self.path:
            try:
                os.remove(self.path)
                return True
            except IOError:
                return False
        else:
            return True

    def md5(self):
        m = hashlib.md5()
        m.update(self.data)
        return m.hexdigest()

    def sha1(self):
        s = hashlib.sha1()
        s.update(self.data)
        return s.hexdigest()

    def extension(self):
        s = mime_search(self)
        return s


class URL(object):
    """ Plugins for this class analyze URLs """
    def __init__(self, url):
        self.url = url

    def get_url_parts(self):
        pass

    def obfuscate(self):
        pass


class Parser(object):
    """ Plugins for this class are used in analysis """
    def __init__(self, analysis_type, result_doc):
        self.analysis_type = analysis_type
        self.result_doc = result_doc

    def traverse(self, data):
        """ This method knows how to recursively traverse 
            an analsys result doc
        """
        if isinstance(data, dict):
            for x in data.values():
                traverse(x)

        elif isinstance(data, list):
            for x in data:
                traverse(x)
        else:
            yield data
            

class Search(object):
    """ Plugins of the class are used to extend searching """
    def __init__(self, query, start, stop, timezone):
        self.query = query
        self.start = start
        self.stop = stop
        self.timezone = timezone


