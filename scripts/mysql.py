from util import *

config = load_config()
config = config['mysql'] if 'mysql' in config else dict()
password = config['password'] if 'password' in config else '123456' 

# Configure mysql
call('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections' % password)
call('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections' % password')

# Install packages from manager
install('mysql-server', 'mysql-client')

# Post config mysql
echo('Post installation configuring MySQL...')
replace('/etc/mysql/my.cnf', 'bind-address', '#ba:')
chown('/etc/mysql/my.cnf', 'mysql', 'mysql')
call('/etc/init.d/mysql restart')
echo('... Done')
