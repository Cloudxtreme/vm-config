from util import *

json_data = load_config()['mongodb']

call('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
call('echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list')
call('apt-get update > /dev/null')
install('mongodb-org=%(v)s mongodb-org-server=%(v)s mongodb-org-shell=%(v)s mongodb-org-mongos=%(v)s mongodb-org-tools=%(v)s' % {'v': json_data['version']})
call('service mongod start')
call('service mongod status')
