from util import *

json_data = load_config()['mysql']

# Configure mysql
call('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections'
     % json_data['password'])
call('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections'
     % json_data['password'])

# Install packages from manager
install('mysql-server', 'mysql-client')

# Post config mysql
echo('Post installation configuring MySQL...')
replace('/etc/mysql/my.cnf', 'bind-address', '#ba:')
chown('/etc/mysql/my.cnf', 'mysql', 'mysql')
call('/etc/init.d/mysql restart')
echo('... Done')
