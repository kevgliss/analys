"""
.. module:: extractor
    :platform: Unix
    :synopsis: A helper module that understands that some zip files submitted
    to Analys will be zips that may be password protected.

    This module is a helper module that understands that
    some zip files submitted to Analys will be zips that may be password
    protected. If this is the case Analys will attempt to bruteforce the password.
    All files contained inside of the zip will submitted individually to Analys.

.. version:: 1.0
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
"""
import os
import zipfile
import rarfile
import logging

from analys.plugins.interfaces import File
from analys.exceptions import EmptyCompressedFile, MaxFileDepth, NoValidPasswordFound
from analys.datastore import Datastore

log = logging.getLogger(__name__)

class Extractor(object):
    """ 
        Extract attempts to identify the password used to
        encrypt a zip file with the most common passwords.
    """
    def __init__(self):
        """
            Initialize the extractor class

            Args:
                file_obj (str): string of bytes
                passwords (list): List of passwords to use
        """
        self.samples = []
        self.max_depth = 4 #only allow four levels of recursion for compressed files
        self.depth = 0

    def fetch_passwords(self):
        return []

    def zip_file(self, file_obj, passwords=None):
        """
            Decompress zip files
        """
        with zipfile.ZipFile(file_obj.create_temp_file(), 'r') as myzip:
            #sanity checks on the file
            log.debug("Zip Members: {}".format(",".join(myzip.namelist())))
            for member in myzip.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue

                if passwords:
                    for password in passwords:
                        try:
                            sample = myzip.open(member, 'r', password).read()
                            break
                        except (zipfile.BadZipfile, RuntimeError) as e:
                            pass
                    else:
                        raise NoValidPasswordFound
                
                else:
                    try:
                        sample = myzip.open(member, 'r').read()
                    except (zipfile.BadZipfile, RuntimeError) as e:
                        raise e
                
                f = File(member, sample)
                log.debug("Member extension: {}".format(f.extension()))
                mime, extension = f.extension()
                if extension in ['zip', 'rar']:
                    log.debug("Found another compressesed file")
                    self.depth = self.depth + 1
                    self.extract(f)
                else:
                    self.samples.append(f)

    def rar_file(self, file_obj, passwords=None):
        """
            Decompress rar files
        """
        with rarfile.RarFile(file_obj.create_temp_file(), 'r') as myrar:
            log.debug("Rar Members: {}".format(",".join(myrar.namelist())))
            for member in myrar.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue

                if passwords:
                    for password in passwords:
                        try:
                            sample = myrar.open(member, 'r', password).read()
                            break
                        except RuntimeError as e:
                            pass
                    else:
                        raise NoValidPasswordFound
                
                else:
                    try:
                        sample = myrar.open(member, 'r').read()
                    except  RuntimeError as e:
                        raise e
                
                f = File(member, sample)
                log.debug("Member extension: {}".format(f.extension()))
                mime, extension = f.extension()
                if extension in ['zip', 'rar']:
                    log.debug("Found another compressesed file")
                    self.depth = self.depth + 1
                    self.extract(f)
                else:
                    self.samples.append(f)
            
    def extract(self, file_obj, passwords=None):
        """
            Extract file

            Args:
                passwords (list): List of passwords to use
            
            Exceptions:
                MaxFileDepth (AnalysException): The recursive limit was met (4)
                EmptyCompressedFile (AnalysException): No files in archive
        """
        if passwords:
            passwords = passwords + self.fetch_passwords()
        
        log.debug("Current depth {}".format(self.depth))
        if self.depth <= self.max_depth:
            if 'zip' in file_obj.extension():
                self.zip_file(file_obj, passwords)
            if 'rar' in file_obj.extension():
                self.rar_file(file_obj, passwords)
        else:
            raise MaxFileDepth
        
        return self.samples

