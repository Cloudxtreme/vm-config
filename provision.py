import platform
import os
import getpass
import apt
from subprocess import *


def echo(message, args=None):
    if not args:
        call(['echo', message])
        return

    call(['echo', message % args])


def install(packages):
    for pkg in packages:
        pkg = cache[pkg]

        if pkg.is_installed:
            echo('%(name)s already installed', {'name': pkg})
        else:
            try:
                call(['apt-get', '-qy', 'install', pkg.name])
                echo('%(name)s installation done', {'name': pkg})
            except Exception, arg:
                echo('Sorry, package installation failed [%(err)s]', {'err': str(arg)})

########################################################################################################################

echo('Provision with Python - %s', platform.python_version())
echo('Guest User Name: %s', getpass.getuser())
echo('Current directory: %s', os.getcwd())

echo('Updating application cache...')
cache = apt.cache.Cache()
cache.update()
echo('... Done')

# Configure mysql
password = '123456'
mysql_package = 'mysql-server'

os.system('echo "%s mysql-server/root_password password %s" | debconf-set-selections' % (mysql_package, password))
os.system('echo "%s mysql-server/root_password_again password %s" | debconf-set-selections' % (mysql_package, password))

# Install packages from manager
pkgs = (mysql_package, 'nano', 'links', 'wget', 'apache2', 'openssl', 'php5', 'php5-mysql', 'libapache2-mod-php5',
        'php5-mcrypt', 'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')
install(pkgs)

# Config mysql
mysql_dir = '/var/lib/mysql/'
if not os.path.isdir(mysql_dir):
    os.mkdir(mysql_dir)

    call(['adduser', 'mysql'])
    call(['chown', 'mysql:mysql', '-R', '/var/lib/mysql'])

########################################################################################################################

echo('Provisioning done')