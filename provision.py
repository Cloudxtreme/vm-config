import platform
from tempfile import mkstemp
from shutil import move
import os
import getpass
import apt
from subprocess import *
import pwd
import grp

password = '123456'

sql_path = "/vagrant/sql"
py_path = "/vagrant/py"

php_ini = '/etc/php5/apache2/php.ini'

########################################################################################################################


def echo(message, args=None):
    if not args:
        call(['echo', message])
        return

    call(['echo', message % args])


def apt_get(packages):
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
pkgs = ('mysql-server', 'nano', 'links', 'wget', 'apache2', 'openssl', 'php5', 'php-pear', 'php5-dev', 'php5-mysql',
        'libapache2-mod-php5', 'php5-mcrypt', 'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')
apt_get(pkgs)

# Post config php
append(php_ini, 'extension=/usr/lib/php5/20121212/mcrypt.so\n')
append(php_ini, 'zend_extension=/usr/lib/php5/20121212/xdebug.so\n')
append(php_ini, 'xdebug.remote_enable=On\n')
os.system('/etc/init.d/apache2 restart')

# Post config mysql
echo('Post installation configuring MySQL...')
replace('/etc/mysql/my.cnf', 'bind-address', '#ba:')
os.chown('/etc/mysql/my.cnf', pwd.getpwnam('mysql').pw_uid, grp.getgrnam('mysql').gr_gid)
os.system('/etc/init.d/mysql restart')
echo('... Done')

# Load SQL scripts
for file_name in os.listdir("%s" % sql_path):
    if file_name.endswith(".sql"):
        echo('Run SQL script: %s/%s' % (sql_path, file_name))
        os.system('mysql -uroot -p%s < %s/%s' % (password, sql_path, file_name))
        echo('Script executed')

# Load Py scripts
for file_name in os.listdir("%s" % py_path):
    if file_name.endswith(".py"):
        echo('Run SQL script: %s/%s' % (py_path, file_name))
        os.system('python %s/%s' % (py_path, file_name))
        echo('Script executed')

########################################################################################################################

echo('Provisioning done')