import pwd
import grp
import getpass
import platform
from tempfile import mkstemp
from shutil import move
import apt
from subprocess import *
import os


def ls(name):
    result = os.listdir(name)
    
    if result is None: 
        return ()

    return result

def chown(name, user, group):
    os.chown(name, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)


def call(command):
    return os.system(command)


def updatedCache():
    echo('Updating application cache...')
    cache = apt.cache.Cache()
    cache.update()
    echo('... Done')


def echo(message, args=None):
    if not args:
        call('echo %s' % message)
        return

    call('echo %s' % (message % args))


def apt_get(packages):
    for pkg in packages:
        pkg = apt.cache.Cache()[pkg]

        if pkg.is_installed:
            echo('%(name)s already installed', {'name': pkg})
        else:
            try:
                call('apt-get -qy install %s' % pkg.name)
                echo('%(name)s installation done', {'name': pkg})
            except Exception, arg:
                echo('Sorry, package installation failed [%(err)s]', {'err': str(arg)})


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
    if not text in open(file_path).read():
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

echo('Provision with Python - %s', platform.python_version())
echo('Guest User Name: %s', getpass.getuser())
echo('Current directory: %s', os.getcwd())
