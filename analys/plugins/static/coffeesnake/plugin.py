"""
.. module:: CoffeeSnake Plugin
    :platform: Unix
    :synopsis: A plugin module used for interaction with CoffeeSnake
.. moduleauthor:: Kevin Glisson <kevin.glisson@gmail.com>
.. version:: 1.0
"""

import logging
log = logging.getLogger(__file__)

import magic
import os
import zipfile
from coffeeSnake import coffeeSnake
from analys.plugins.interfaces import File

class AnalysPlugin(object):
    """
    :param url: url
    :type url: str
    """
    def __init__(self, *args, **kwargs):
        self.file = File(kwargs['data'])

    def submit(self):
        #try:
            file_path = self.file.create_temp_file()
            cf = coffeeSnake()
            filetype = magic.from_file(file_path)

            if zipfile.is_zipfile(file_path):
                jar = zipfile.ZipFile(file_path)

                jar.extractall(file_path + '.jar')
                print file_path
                disasm_datas = cf.processDirectory(file_path + '.jar')
            elif os.path.isdir(file_path) or \
                    filetype.startswith('compiled Java class data'):
                disasm_datas = cf.processDirectory(file_path)
            else:
                return False

            results = { "Suspicious":[],
                        "Instructions":[],
                        "No Match": [],
                        "Not Suspicious":[],
                        "Files Processed":0  }

            for thisfile in disasm_datas:
                disasm_data = disasm_datas[thisfile]
                matches = cf.detectBad(disasm_data)
                if matches:
                    for instruction in matches:
                        for yaradict in matches[instruction]:
                            for index in yaradict:
                                offset =0
                                match = yaradict[index]
                                matchdata = disasm_data[instruction][index]
                                cve = ''
                                if 'ref' in match.meta:
                                    cve = match.meta['ref']
                                matchString = ('%s file %s' % (match,thisfile),
                                        '%s instruction %s' % (cve, instruction))
                                results['Match'].append(matchString)

                                for offset in match.strings:
                                    offsetString = '\tinstruction instance %d, arg offset %d: matches "%s"' % (index,offset,re.sub('[\x00-\x19\n\x7f-\xff]','.',match.strings[offset]))
                                    results['Instructions'].append(offsetString)

                                        #not using matchdata[offset:]
                else:
                    results["No Match"].append(thisfile)
            results["Files Processed"] = (cf.processedClassFiles)

            #subprocess.call(['rm','-r',filePath+'x/'])
            #subprocess.call(['rm','-r',cf.tmpdir])

            return results
        #except:
        #  log.error("CoffeeSnake Failed", exc_info=True)
