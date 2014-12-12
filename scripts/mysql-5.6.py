from util import *

root_password = '123456'

user = 'root'
password = '123456'

# Configure mysql
call('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections' % root_password)
call('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections' % root_password)

# Install packages from manager

pkgs = ('mysql-server-5.6', 'mysql-client-5.6')
apt_get(pkgs)

# Post config mysql
echo('Post installation configuring MySQL...')
replace('/etc/mysql/my.cnf', 'bind-address', '#ba:')
chown('/etc/mysql/my.cnf', 'mysql', 'mysql')
call('/etc/init.d/mysql restart')

if user == 'oot':
    # TODO: Add user
    print 'User creation not implemented'

queries = [
    'create user %(user)s@10.0.2.2 identified by "%(password)s";',
    'grant all privileges on *.* to %(user)s@10.0.2.2 with grant option;',
    'flush privileges;',

    'select user, host from mysql.user where user="%(user)s";'
]

for query in queries:
    call("mysql -uroot -p%(password)s -e '%(query)s'" % {
        "password": root_password,
        "query": query % {"user": user, "password": password}
    })

echo('... Done')