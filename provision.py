import platform
import os
import getpass
import apt
from subprocess import call
import sys

print "Provision with Python - " + platform.python_version()
print "Guest User Name: " + getpass.getuser()
print "Current directory: " + os.getcwd()

print "Updating application cache..."
cache = apt.cache.Cache()
cache.update()
print "... Done"


def install(pkgs):
    for pkg in pkgs:
        pkg = cache[pkg]

        if pkg.is_installed:
            print '%(name)s already installed' % {'name': pkg}
        else:
            try:
                call(["apt-get", "-y", "-f", "install", pkg.name])
                print '%(name)s installation done' % {'name': pkg}
            except Exception, arg:
                print >> sys.stderr, "Sorry, package installation failed [%(err)s]" % {'err': str(arg)}


pkgs = ('nano', 'links', 'wget', 'apache2', 'openssl', 'php5', 'php5-mysql', 'libapache2-mod-php5', 'php5-mcrypt', 'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')
install(pkgs)

# Install MySql
mysql_dir = "/usr/lib/mysql"
mysql_file = "mysql-5.6.21-linux-glibc2.5-x86_64"
mysql_source = "http://dev.mysql.com/get/Downloads/MySQL-5.6"
if not os.path.isdir(mysql_dir):
    print "Installing MySQL"
    os.mkdir(mysql_dir)
    os.chdir(mysql_dir)

    print "Downloading..."
    call(["wget", "%(source)s/%(file)s.tar.gz" % {'source': mysql_source, 'file': mysql_file}, "-nv"])
    print "... Done"

    call(["tar", "-xzf", "%s.tar.gz" % mysql_file])
    call(["mv", "./%s/*" % file, "."])

    call(["rm", "-r", mysql_file])
    call(["rm", "-r", "%s.tar.gz" % mysql_file])
else:
    print 'MySQL already installed'
