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
log = logging.getLogger(__file__)

class Extractor(object):
    """ Extract attempts to identify the password used to
        encrypt a zip file. The most common passwords.

        :param data: raw file bytes
        :type data: byte string

    """
    def __init__(self, file, passwords):
        self.file = file
        self.samples = []
        self.max_depth = 5 #only allow five levels of recursion for compressed files
        self.depth = 0
        self.passwords = passwords

    def extract(self):
        if self.depth <= self.max_depth:
            if 'zip' in self.file.extension():
                with zipfile.ZipFile(self.file.create_temp_file(), 'r') as myzip:
                    #sanity checks on the file
                    for member in myzip.namelist():
                        filename = os.path.basename(member)
                        if not filename:
                            continue

                        try:
                            sample = myzip.open(member, 'r',).read()
                            f = File(member, sample)
                            if f.extension() in ['zip', 'rar']:
                                self.depth = self.depth + 1
                                self.extract(f)
                            else:
                                self.samples.append(f)

                        except (zipfile.BadZipfile, RuntimeError) as err:
                            for password in self.passwords:

                                try:
                                    sample = myzip.open(member, 'r', password).read()
                                    f = File(member, sample)
                                    if f.extension() in ['zip', 'rar']:
                                        self.depth = self.depth + 1
                                        self.extract(f)
                                    else:
                                        self.samples.append(f)
                                    break

                                except (zipfile.BadZipfile, RuntimeError) as err:
                                    continue

            if 'rar' in self.file.extension():
                with rarfile.RarFile(self.file.create_temp_file(), 'r') as myrar:
                    #sanity checks on the file
                    for member in myrar.infolist():
                        if not member.filename:
                            continue
                        try:
                            sample = myrar.open(member, 'r').read()
                            f = File(member, sample)
                            if f.extension() in ['zip', 'rar']:
                                self.depth = self.depth + 1
                                self.extract(f)
                            else:
                                self.samples.append(f)
                        except:
                            for password in self.passwords:
                                try:
                                    sample = myrar.open(member, 'r',
                                            password).read()
                                    f = File(member, sample)
                                    if f.extension() in ['zip', 'rar']:
                                        self.depth = self.depth + 1
                                        self.extract(f)
                                    else:
                                        self.samples.append(f)
                                    break
                                except:
                                    continue
        return self.samples

