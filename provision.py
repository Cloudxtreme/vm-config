import platform
import os
import getpass
import apt
from subprocess import *

# Configured
password = '123456'

sql_path = "/vagrant/sql"
py_path = "/vagrant/py"


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
os.system('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections' % password)
os.system('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections' % password)

# Install packages from manager
pkgs = ('mysql-server', 'nano', 'links', 'wget', 'apache2', 'openssl', 'php5', 'php5-mysql', 'libapache2-mod-php5',
        'php5-mcrypt', 'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')
install(pkgs)

# Load SQL scripts
for file in os.listdir("%s" % sql_path):
    if file.endswith(".sql"):
        echo('Run SQL script: %s/%s' % (sql_path, file))
        os.system('mysql -uroot -p%s < %s/%s' % (password, sql_path, file))
        echo('Script executed')

# Load Py scripts
for file in os.listdir("%s" % py_path):
    if file.endswith(".py"):
        echo('Run SQL script: %s/%s' % (py_path, file))
        os.system('python %s/%s' % (py_path, file))
        echo('Script executed')

########################################################################################################################

echo('Provisioning done')