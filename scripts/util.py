import pwd
import grp
import getpass
import platform
from tempfile import mkstemp
from shutil import move
import os
import json
from mmap import mmap

root_dir = os.path.dirname(os.path.abspath(__file__)).replace('scripts', '')

# Config and loading utils
def load_config():
    json_data = open(root_dir + 'config.json')
    config = json.load(json_data)
    json_data.close()

    return config

# Command line utils
def ls(name):
    result = os.listdir(name)
    
    if result is None: 
        return ()

    return result


def install(*args):
    query = ''
    for arg in args:
        query = "%s %s" % (query, arg)

    call('apt-get -q -y install %s' % query)


def chown(name, user, group):
    os.chown(name, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)


def call(*args):
    query = ''

    for arg in args:
        query = ('%s && %s' % (query, arg)) if query else arg

    echo(query)
    return os.system(query)


def echo(message, args=None):
    if not args:
        os.system('echo "%s"' % message)
        return

    os.system('echo "%s"' % (message % args))

# Files utils
def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file_path)

    for line in old_file:
        new_file.write(line.replace(pattern, subst))

    new_file.close()
    os.close(fh)
    old_file.close()

    os.remove(file_path)
    move(abs_path, file_path)


def append(file_path, text):
    if text not in open(file_path).read():
        with open(file_path, "a") as myfile:
            echo('Adding %s to file %s' % (text, file_path))
            myfile.write(text)
    else:
        echo('%s already in file %s' % (text, file_path))


def chmod(path, rights):
    os.chmod(path, rights)
    for target, d, f in os.walk(path):
        try:
            os.chmod(target, rights)
        except Exception:
            echo('Can\'t change right to %s' % target)


def insert(filename, str, target):
    if len(str) < 1:
        return

    f = open(filename, 'r+')
    m = mmap(f.fileno(), os.path.getsize(filename))
    size = m.size()
    pos = m.find(target) + len(target)

    if pos > size or pos < 0:
        pos = size
        
    m.resize(size + len(str))
    m[pos + len(str):] = m[pos:size]
    m[pos:pos + len(str)] = str
    m.close()
    f.close()            


def replace_after(filename, str_origin, str_replace, target):
    if len(str_origin) < 1 or len(str_replace) < 1 :
        return

    f = open(filename, 'r+')
    m = mmap(f.fileno(), os.path.getsize(filename))
    size = m.size()
    pos = m.find(str_origin, m.find(target) + len(target))
    tmp = m[pos:size]

    size_dif = len(str_replace) - len(str_origin)
    m.resize(size + size_dif)

    m[pos + len(str_replace):] = tmp
    m[pos:pos + len(str_replace)] = str_replace
    m.close()
    f.close()  


def find(name, location='/'):
    result = set()
    
    for root, dirs, files in os.walk(location):
        for file in files:
            if file is name:
                 result.add(file)
                 
    return result


def find_first(name, location='/'):
    for root, dirs, files in os.walk(location):
        for file in files:
            if file is name:
                 return file
    
    return None
    
# Execution info
echo('Provision with Python - %s', platform.python_version())
echo('Guest User Name: %s', getpass.getuser())
echo('Current directory: %s', os.getcwd())
