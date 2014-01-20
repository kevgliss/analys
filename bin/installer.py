#!/usr/bin/env python

import os
import sys
import redis
# import shutil
import pymongo
import platform
import distutils
import subprocess

def install():
    term_width, term_height = getTerminalSize()
    if not term_width:
        term_width = 0

    config = {'install_dir': '/opt/',
              'mongodb': {'hostname': '127.0.0.1', 'port': 27017},
              'redis': {'hostname': '127.0.0.1', 'port': '6379'}}

    print '  ______                       __                        '.center(term_width)
    print ' /      \                     |  \                       '.center(term_width)
    print '|  $$$$$$\ _______    ______  | $$ __    __   _______    '.center(term_width)
    print '| $$__| $$|       \  |      \ | $$|  \  |  \ /       \\   '.center(term_width)
    print '| $$    $$| $$$$$$$\  \$$$$$$\| $$| $$  | $$|  $$$$$$$   '.center(term_width)
    print '| $$$$$$$$| $$  | $$ /      $$| $$| $$  | $$ \$$    \    '.center(term_width)
    print '| $$  | $$| $$  | $$|  $$$$$$$| $$| $$__/ $$ _\$$$$$$\\   '.center(term_width)
    print '| $$  | $$| $$  | $$ \$$    $$| $$ \$$    $$|       $$   '.center(term_width)
    print ' \$$   \$$ \$$   \$$  \$$$$$$$ \$$ _\$$$$$$$ \$$$$$$$    '.center(term_width)
    print '                                  |  \__| $$             '.center(term_width)
    print '                                   \$$    $$             '.center(term_width)
    print '                                    \$$$$$$              '.center(term_width)

    print 'Welcome to Analys we will first get started by asking for some information.\n'

    # Set install path
    install_path = raw_input('Where would you like to install Analys? Must be full path. ({}): '.format(config['install_dir']))
    if install_path:
        if install_path.endswith('/'):
            config['install_dir'] = install_path
        else:
            config['install_dir'] = install_path + '/'

    # try to guess what we are about to install on
    env = platform.system()
    if env in 'Darwin':
        if subprocess.call(['which', 'brew']) == 1:
            brew = raw_input('[+] Analys uses the homebrew package manager to install dependencies on OSX. Install it now? (Y/n)')
            if brew.lower() in 'y':
                os.system('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
            else:
                sys.exit(1)
        print '[+] Updating homebrew...' 
        subprocess.call(['brew', 'update'])
    
    # Update ubuntu packages
    # TODO: determine different linux distros, will only work on ubuntu atm
    elif 'linux' in env.lower():
        print '[+] Updating packages...'
        subprocess.call(['apt-get', 'update'])
        subprocess.call(['apt-get', 'install', '-y', 'python-software-properties'])

    # Install/test mongodb
    if 'n' in raw_input('[+] Would you like to try and install mongodb on this system? (Y/n)').lower():

        # Get hostname
        hostname = raw_input('[+] What is the hostname of your mongodb instance or replicaset? ({})'.format(config['mongodb']['hostname']))
        if hostname:
            config['mongodb']['hostname'] = hostname
            
        # Get port
        port = raw_input('[+] What port is mongodb running on? ({})'.format(config['mongodb']['port']))
        if port:
            config['mongodb']['port'] = port

        # Try connecting to MongoDB
        print '[+] Attempting to contact the specified host...'
        try:
            client = pymongo.MongoClient(config['mongodb']['hostname'], config['mongodb']['port'])
        except pymongo.errors.ConnectionFailure:
            print '[-] Mongodb connection failed!'
            sys.exit()

        # We were able to successfully connect
        print '[+] Great Success!'

    else:
        if env in 'Darwin':
            if subprocess.call(['which', 'mongo']) == 1:
                if subprocess.call(['brew', 'install','mongodb']) == 0:
                    print '[+] Mongodb installed'
                else:
                    print '[-] Mongodb installation failed'
            else:
                print '[+] Mongodb is already installed'

        # TODO: handle other linux distros
        elif 'linux' in env.lower():
            
            # Import the MongoDB public GPG Key
            subprocess.call(['apt-key', 'adv', '--keyserver', 'hkp://keyserver.ubuntu.com:80', '--recv', '7F0CEB10'])
            
            # Create a /etc/apt/sources.list.d/mongodb.list file
            p1 = subprocess.Popen(['echo', 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen'], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['tee', '/etc/apt/sources.list.d/mongodb.list'], stdin=p1.stdout)
            p1.stdout.close()
            p2.communicate()

            # Update packages
            subprocess.call(['apt-get', 'update'])

            # Install mongodb
            subprocess.call(['apt-get', 'install', 'mongodb-10gen'])

    # Install/test redis
    if 'n' in raw_input('[+] Would you like to try and install redis on this system? (Y/n)').lower():

        # Get hostname
        hostname = raw_input('[+] What is the hostname of your redis instance? ({})'.format(config['redis']['hostname']))
        if hostname:
            config['redis']['hostname'] = hostname

        # Get port
        port = raw_input('[+] What port is redis running on? ({})'.format(config['redis']['port']))
        if port:
            config['redis']['port'] = port
        
        # Try connecting to reddis
        print '[+] Attempting to contact the specified host...'
        try:
            rs = redis.StrictRedis(host=config['redis']['hostname'], port=int(config['redis']['port']), db=0)
            response = rs.client_list()
        except redis.exceptions.ConnectionError:
            print '[-] Redis connection failed!'
            sys.exit()

        # We were able to successfully connect
        print '[+] Great Success!'

    else: 
        if env in 'Darwin':
            if subprocess.call(['which', 'redis-server']) == 1:
                if subprocess.call(['brew', 'install', 'redis']) == 0:
                    print '[+] Redis installed'
                else:
                    print '[-] Redis installation failed'
            else:
                print '[+] Redis already installed'
         
        # TODO: handle other linux distros
        elif 'linux' in env.lower():
            
            # Add reddis repo
            subprocess.call(['add-apt-repository', '-y', 'ppa:rwky/redis'])
            subprocess.call(['apt-get', 'update'])

            # Install mongodb
            subprocess.call(['apt-get', 'install', '-y', 'redis-server'])
    
    # Copy files into install directory
    print '[+] Installing Analys into {}'.format(config['install_dir'])
    print 'Install directory:', os.path.join(config['install_dir'], 'analys')
    try:
        os.makedirs(config['install_dir'])
    except OSError:
        pass
    cwd = os.path.dirname(os.path.realpath(__file__))
    subprocess.call(['cp', '-r', os.path.split(cwd)[0], os.path.join(config['install_dir'], 'analys')])
    
    # Make sure files were copied
    try:
       with open(os.path.join(config['install_dir'], 'analys', 'setup.py')):
           print '[+] Analys has been successfully installed'
    except IOError:
       print '[-] Analys could not be installed. Do you have the right permissions?'

   # Populate database with default settings
    print '[+] Populating datastore with default settings'

    types = [('application/msword','doc'),
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
    
def remove():
    # Why would anyone ever want to remove analys?
    pass

def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

if __name__ == '__main__':
    arg = sys.argv[1]
    if 'install' in arg:
        install()
    elif 'remove' in arg:
        remove()