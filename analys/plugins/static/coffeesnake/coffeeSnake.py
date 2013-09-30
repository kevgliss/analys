#!/usr/bin/python
'''
Author:         Blake Hartstein
Program name:   coffeeSnake v0.1
Company:        iDefense 2010

Props:          Greg Sinclair for the name of "coffeeSnake"
'''
import glob,magic,os,time,sys
import zipfile,subprocess
import yara,re,string

class coffeeSnake:
    '''
        coffeeSnake class is useful for detecting malicious and suspicious Java files
        Each of the process(.*) functions acts in an identical manner with slightly different inputs or outputs.
        After processing a file or data, just call the detectBad() function.

        The self.processedFiles variable might be useful if you use processDirectory, then afterwards want to save the
        java class filenames you just processed. You can output those to a newline separated file then process that file with
        processFileList. This will save time by avoiding determining the filetypes again, but does not locate new files.
    '''
    def __init__(self):
        self.tmpdir = './tmpjava/'
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)
        self.processedFiles = [] # populated with all entries for each Java class files processed during the life of the program
        self.processedClassFiles = 0 #counter

        #initialize magic library
        #self.ms = magic.open(magic.MAGIC_NONE)
        #self.ms.load()

        ruledata = '''
        rule getSoundbank
        {
            meta:
                ref = "CVE-2009-3867"
            strings:
                $a = "MidiSystem.getSoundbank" fullword
            condition:
                1 of them
        }
        /* ///This calendarObject rule is disabled because
           ///most of the calendar exploits in the wild
           ///do not directly access the object and are often
           ///obfuscated. Also there are more legitimate accesses
           ///to calendar objects.
        rule calendarObject
        {
            meta:
                ref = "CVE-2008-5353"
            strings:
                $a = "calendar" nocase
            condition:
                1 of them
        }
        */
        rule RMIConnectionImpl
        {
            meta:
                ref = "CVE-2010-0094"
            strings:
                $a = "RMIConnectionImpl"
            condition:
                1 of them
        }
        rule SuspiciousMethod
        {
            strings:
                $a = "java/security/AccessController.doPrivileged"
                $b = "java/lang/Runtime.exec"
                $c = "java/lang/Runtime.load"
                $d = "java/security/AllPermission"
            condition:
                1 of them
        }
        rule ObfuscationMethod
        {
            strings:
                $a = /String [^\\n'\],\/]{100}/
            condition:
                1 of them
        }
        rule DiscoveredURL
        {
            strings:
                $a = /http:\/\/[^\\x00-\\x20\\x7f-\\xff]+/
            condition:
                1 of them
        }
        '''
        self.rules = yara.compile(source = ruledata)


    def processData(self,data, filename = ''):
        '''
            Pre: Use Java class file or Zip contents (for a JAR file) in data
            Post:
                Creates a temporary file within self.tmpdir directory
                Disassembles the file using javap -c
                Returns a dictionary grouping the disassembly using the instruction as the key and contents of all unique arguments
        '''

        java_files = []

        #make sure these are indeed java class files, otherwise ignore them
        filetype = magic.from_buffer(data)#self.ms.buffer(data)
        if filetype and filetype.startswith('Zip archive data'):
            try:
                fout = open(self.tmpdir + 'tmp.zip','wb')
                fout.write(data)
                fout.close()
                zip = zipfile.ZipFile(self.tmpdir+'tmp.zip')

                enclosed_files = zip.namelist()
                if len(enclosed_files) > 20:
                    print >>sys.stderr, '%s has %d enclosed_files (>20), skipping' % (filename, len(enclosed_files))
                else:
                    for infile in enclosed_files:
                        if infile.endswith('.class'):
                            fin = zip.open(infile,'r')
                            java_files.append(fin.read())
                            fin.close()
            except zipfile.BadZipfile:
                print >>sys.stderr, '%s not a valid zip' % (filename)
        elif filetype and filetype.startswith('compiled Java class data'):
            java_files.append(data)

        #begin processing the java class files
        prop = {}
        for filedata in java_files:
            filetype = magic.from_buffer(data)#self.ms.buffer(filedata)

            if filetype and filetype.startswith('compiled Java class data'):

                if filename and (not filename in self.processedFiles):
                    self.processedFiles.append(filename)
                self.processedClassFiles += 1

                base_file = self.tmpdir + 'tmp_java_file'
                fout = open(base_file +'.class','wb')
                fout.write(filedata)
                fout.close()

                javap_stdout = open(base_file + '.stdout','wb')
                javap_stderr = open(base_file + '.stderr','wb')
                po = subprocess.Popen(['javap', '-c', base_file], shell=False, stdout = javap_stdout, stderr = javap_stderr, close_fds=True)

                while po.poll() == None:
                    time.sleep(1)

                javap_stdout.close()
                javap_stdout = open(base_file + '.stdout','rb')
                decoded = javap_stdout.read()
                javap_stdout.close()

                javap_stderr.close()
                javap_stderr = open(base_file + '.stderr','rb')
                errors = javap_stderr.read()
                javap_stderr.close()

                for line in decoded.split('\n'):
                    #line:    7182:  ldc_w   #647; //String _b25a3fe9ce0d61d
                    tabbed = line.split('\t')
                    if len(tabbed) > 1:
                        args = []
                        if len(tabbed) > 2:
                            asm = tabbed[1]
                            args = tabbed[2:]

                        elif tabbed[1].find(' ') > -1:
                            if args:
                                print >>sys.stderr,'%s warning args in multiple places, discarding %s' % (filename, args)
                            spaces = tabbed[1].split(' ')
                            asm = spaces[0]
                            args = spaces[1:]
                        else:
                            asm = args = ''
                        args = string.join(args) #flatten args into a single string

                        if asm:
                            if not asm in prop:
                                prop[asm] = []
                            if not args in prop[asm]:
                                prop[asm].append(args)
                    #else:
                    #    print 'class definition line ', line
        return prop

    def processFile(self,filename):
        '''
            Pre: filename is a Java class file or Zip file (for a JAR file)
            Post: Helper function for processData
        '''
        fin = open(filename,'rb')
        filedata = fin.read()
        fin.close()
        return self.processData(filedata,filename)

    def processFileList(self,filename):
        '''
            Pre: Filename is a file that contains a list of filenames to process
                 separated by newlines
            Post:
                Helper function for processFile and processData
                Duplicate filenames in the list are ignored
                Returns a dictionary with filename processed as keys
        '''
        fin = open(filename,'r')
        files = fin.read().split('\n')
        fin.close()

        result = {}
        for file in files:
            if not file in result:
                if file and os.path.exists(file):
                    result[file] = self.processFile(file)
        return result
    def processDirectory(self,startdir):
        '''
            Pre: startdir is either a directory or a single file
            Post:
                Helper function for processFile (and subsequently processData)
                Returns a dictionary with filename processed as keys
        '''
        result = {}
        if os.path.exists(startdir):
            if os.path.isdir(startdir):
                for r, d, fs in os.walk(startdir):
                    for f in fs:
                        result[os.path.join(r,f)] = self.processFile(os.path.join(r,f))

            elif os.path.isfile(startdir):
                result[startdir] = self.processFile(startdir)
        return result

    def detectBad(self,prop):
        '''
            Pre: prop is a dictionary obtained from one of the processData, processFile, or processFileList routines.
                Uses self.rules yara object from __init__(...)
            Post: Returns a dictionary indexed by instruction name.
                result = {
                        'instructionName1': [
                                            { 0 : {
                                                    offset: yaraMatchObject1
                                                  }, #### 0 and 1 are indexes to the prop dictionary elements
                                           ],
                        'instructionName2': [...],
                        }
        '''
        result = {}
        for key in prop:
                #for arguments in prop[key]:
                argindex = 0
                for argument in prop[key]: #arguments:
                    matches = self.rules.match(data=argument)
                    for m in matches:
                        if not key in result:
                            result[key] = []
                        result[key].append( {argindex : m} )
                    argindex += 1
        return result


if __name__ == '__main__':
    ''' A basic demonstration of what the coffeeSnake class can do. It accepts filename arguments on the command-line. '''
    cf = coffeeSnake()
    for arg in sys.argv[1:]:

        #ms = magic.open(magic.MAGIC_NONE)
        #ms.load()
        filetype = magic.from_file(arg)#ms.file(arg)

        if os.path.isdir(arg) or filetype.startswith('compiled Java class data'):
            disasm_datas = cf.processDirectory(arg)
        else:
            usage = 'Invalid command line: argument is not a \n\t1) directory\n\t2) Java class file\n\t3) file containing a list of filepaths'
            fin = open(arg,'r')
            first_line = fin.read().split('\n')[0]
            fin.close()
            if os.path.exists(first_line):
                disasm_datas = cf.processFileList(arg)
            else:
                print usage
                exit(1)


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
                            print '%s file %s, %s instruction %s' % (match,thisfile,cve,instruction)
                            for offset in match.strings:
                                print '\tinstruction instance %d, arg offset %d: matches "%s"' % (index,offset,re.sub('[\x00-\x19\n\x7f-\xff]','.',match.strings[offset]))
                                #not using matchdata[offset:]
            else:
                print 'NoMatch file %s' % (thisfile)
    print 'There were %d Java class files processed' % (cf.processedClassFiles)

