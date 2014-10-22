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
mysql_package = 'mysql-server-5.5'

p1 = Popen(['echo', '"%s mysql-server/root_password password %s"' % (mysql_package, password)], stdout=PIPE)
p2 = Popen(['debconf-set-selections'], stdin=p1.stdout)
p1.stdout.close()
p2.communicate()

p3 = Popen(['echo', '"%s mysql-server/root_password password %s"' % (mysql_package, password)], stdout=PIPE)
p4 = Popen(['debconf-set-selections'], stdin=p3.stdout)
p3.stdout.close()
p4.communicate()

# Install packages from manager
pkgs = (
    'nano', 'links', 'wget', 'apache2', 'openssl', 'php5', 'php5-mysql', 'libapache2-mod-php5', 'php5-mcrypt',
    'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug', mysql_package)
install(pkgs)

########################################################################################################################

echo('Provisioning done')