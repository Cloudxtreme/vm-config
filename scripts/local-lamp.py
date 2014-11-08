from util import *

password = '123456'

sql_path = "/vagrant/sql"
py_path = "/vagrant/py"

php_ini = '/etc/php5/apache2/php.ini'

# Configure mysql
call('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections' % password)
call('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections' % password)

# Install packages from manager
pkgs = ('mysql-server', 'nano', 'links', 'wget', 'apache2', 'openssl', 'php5', 'php-pear', 'php5-dev', 'php5-mysql',
        'libapache2-mod-php5', 'php5-mcrypt', 'php5-curl', 'php5-common', 'php5-cgi', 'php5-gd', 'php5-xdebug')
apt_get(pkgs)

# Post config php
append(php_ini, 'extension=/usr/lib/php5/20121212/mcrypt.so\n')
append(php_ini, 'zend_extension=/usr/lib/php5/20121212/xdebug.so\n')
append(php_ini, 'xdebug.remote_enable=On\n')
call('/etc/init.d/apache2 restart')

# Post config mysql
echo('Post installation configuring MySQL...')
replace('/etc/mysql/my.cnf', 'bind-address', '#ba:')
chown('/etc/mysql/my.cnf', 'mysql', 'mysql')
call('/etc/init.d/mysql restart')
echo('... Done')

# Load SQL scripts
for file_name in ls(sql_path):
    if file_name.endswith(".sql"):
        echo('Run SQL script: %s/%s' % (sql_path, file_name))
        call('mysql -uroot -p%s < %s/%s' % (password, sql_path, file_name))
        echo('Script executed')

echo('Provisioning done')
