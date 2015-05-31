from util import *

php_ini = '/etc/php5/apache2/php.ini'

# Install packages from manager
install('apache2', 'php5', 'php-pear', 'php5-dev', 'php5-mysql', 'libapache2-mod-php5',
        'php5-mcrypt', 'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')

# Post config php
append(php_ini, 'extension=%s\n' % find_first('mcrypt.so', '/usr/lib/php5'))
append(php_ini, 'zend_extension=%s\n' % find_first('xdebug.so', '/usr/lib/php5'))

append(php_ini, 'xdebug.remote_enable=On\n')
append(php_ini, 'xdebug.remote_connect_back=On\n')
append(php_ini, 'xdebug.idekey="vagrant"\n')

call('a2enmod rewrite')

replace_after('/etc/apache2/apache2.conf', 'AllowOverride None', 'AllowOverride All', '<Directory /var/www/>')

call('service apache2 restart')
call('service php5-fpm restart')
