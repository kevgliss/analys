"""
.. module:: mimesfinder
    :platform: Unix
    :synopsis: This module is a container module that holds
               all mime types that analys is able to handle

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>

"""

import magic
import zipfile

#TODO Store valid types in datastore
ANALYS_TYPES = [('application/msword','doc'),
            ('application/msword','doc'),
            ('application/vnd.ms-office','doc'),
            ('application/vnd.openxmlformats-officedocument.wordprocessingml.document','doc'),
            ('application/vnd.openxmlformats-officedocument.wordprocessingml.template','doc'),
            ('application/vnd.ms-word.document.macroEnabled.12','doc'),
            ('application/vnd.ms-word.template.macroEnabled.12','doc'),
            ('application/vnd.ms-excel','xls'),
            ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','xls'),
            ('application/vnd.openxmlformats-officedocument.spreadsheetml.template','xlst'),
            ('application/vnd.ms-excel.sheet.macroEnabled.12','xlsx'),
            ('application/vnd.ms-excel.template.macroEnabled.12','exlsxt'),
            ('application/vnd.ms-excel.addin.macroEnabled.12','xlsx'),
            ('application/vnd.ms-excel.sheet.binary.macroEnabled.12','xlsx'),
            ('application/vnd.ms-powerpoint','ppt'),
            ('application/vnd.openxmlformats-officedocument.presentationml.presentation','ppt'),
            ('application/vnd.openxmlformats-officedocument.presentationml.template','pptt'),
            ('application/vnd.openxmlformats-officedocument.presentationml.slideshow','ppt'),
            ('application/vnd.ms-powerpoint.addin.macroEnabled.12','pptx'),
            ('application/vnd.ms-powerpoint.presentation.macroEnabled.12','pptx'),
            ('application/vnd.ms-powerpoint.template.macroEnabled.12','pptx'),
            ('application/vnd.ms-powerpoint.slideshow.macroEnabled.12','pptx'),
            ('text/rtf', 'rtf'),
            ('application/exe', 'exe'),
            ('application/x-dosexec', 'exe'),
            ('application/x-executable', 'exe'),
            ('application/pdf','pdf'),
            ('application/swf', 'swf'),
            ('application/x-shockwave-flash','swf'),
            ('text/javascript', 'js'),
            ('application/x-jar', 'jar'),
            ('application/x-java-applet', 'jar'),
            ('application/vnd.android.package-archive', 'apk'),
            ('application/zip', 'zip'),
            ('application/x-rar', 'rar'),
            ('text/html', 'html'),
            ('text/plain', 'html')]

#These are binary types use magic to guess
MAGIC_TYPES = [('Zip archive data', 'application/zip'),
               ('MS Windows HtmlHelp Data', 'text/html')]

def search(file):
    """ Search attempt to identify a filetype category for a
        particular file. It uses a list of known mime types and a
        files magic byte to make that determination.

        It also handles zips and rars files with limited functionality. In
        that it will peek inside zip files and try to determine the
        type of file contained within

        :param data: raw file bytes
        :type data: byte string

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

    for analys_mime, extension in ANALYS_TYPES:
        if mime in analys_mime:
            if extension == 'zip':
                extension = _peek_compressed(file)
                return (mime, extension)
            else:
                return (mime, extension)
    return (None, None)
