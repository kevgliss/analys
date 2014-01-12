"""
.. module:: mime
    :platform: Unix
    :synopsis: This module is a container module that holds
               all mime types that analys is able to handle

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>

"""

import magic
import zipfile
import logging

from analys.common.settings import Settings
from analys.exceptions import InvalidMimeType
from analys.common.utils import get_datastore

log = logging.getLogger(__name__)

#These are binary types use magic to guess
MAGIC_TYPES = [('Zip archive data', 'application/zip'),
               ('MS Windows HtmlHelp Data', 'text/html')]

#TODO Store valid types in datastore/config
#TODO finish unit test
def get_file_types():
    s = Settings(get_datastore())
    return s.get_mimetype_mappings()

def search(file):
    """ 
        Search attempt to identify a filetype category for a
        particular file. It uses a list of known mime types and a
        files magic byte to make that determination.

        It also handles zips and rars files with limited functionality. In
        that it will peek inside zip files and try to determine the
        type of file contained within

        Args:
            file (str): raw file bytes

        Returns:
            tuple (str, str): Mime and extensions of a given byte string
    """
    def _peek_compressed(file):
        tmpfile = file.create_temp_file()
        #Look inside the zip
        with zipfile.ZipFile(tmpfile, 'r') as myzip:
            # check for jar and apk files
            if 'AndroidManifest.xml' in myzip.namelist():
                return 'apk'
            for x in myzip.namelist():
                if x.endswith('class'):
                    return 'jar'
        return 'zip'

    mime = magic.from_buffer(file.data, mime=True)
    #we have a binary type use magic to guess
    if mime in 'application/octet-stream':
        app = magic.from_buffer(data)
        for guess, valid_mime in MAGIC_TYPES:
            if app == guess:
                mime = valid_mime

    for analys_mime, extension in get_file_types():
        if mime in analys_mime:
            if extension == 'zip':
                extension = _peek_compressed(file)
                return (mime, extension)
            else:
                return (mime, extension)
    log.info("Invalid mimetype: {}".format(mime))
    raise InvalidMimeType
