from util import *

password = '123456'

# Configure mysql
call('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections' % password)
call('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections' % password)

# Install packages from manager

pkgs = ('mysql-server-5.6', 'mysql-client-5.6')
apt_get(pkgs)

# Post config mysql
echo('Post installation configuring MySQL...')
replace('/etc/mysql/my.cnf', 'bind-address', '#ba:')
chown('/etc/mysql/my.cnf', 'mysql', 'mysql')
call('/etc/init.d/mysql restart')
echo('... Done')
