from util import *

json_data = load_config()
json_data = json_data['mongodb'] if 'mongodb' in json_data else dict()

call('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
call('echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list')
call('apt-get update > /dev/null')

if 'version' in json_data:
  call('apt-get install -y mongodb-org=%(v)s mongodb-org-server=%(v)s mongodb-org-shell=%(v)s mongodb-org-mongos=%(v)s mongodb-org-tools=%(v)s' % {'v': json_data['version']})
else:
  call('apt-get install -y mongodb-org')

call('service mongod start')
call('service mongod status')
