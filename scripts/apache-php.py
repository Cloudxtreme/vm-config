from util import *

php_ini = '/etc/php5/apache2/php.ini'

# Install packages from manager
pkgs = ('apache2', 'php5', 'php-pear', 'php5-dev', 'php5-mysql', 'libapache2-mod-php5', 'php5-mcrypt', 
        'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')
apt_get(pkgs)

# Post config php
append(php_ini, 'extension=/usr/lib/php5/20121212/mcrypt.so\n')
append(php_ini, 'zend_extension=/usr/lib/php5/20121212/xdebug.so\n')
append(php_ini, 'xdebug.remote_enable=On\n')
call('/etc/init.d/apache2 restart')
