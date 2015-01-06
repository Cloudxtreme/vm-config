from util import *

json_data = load_config()['java']

call('echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections')
call('echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections')

call('apt-get -qy remove openjdk* > /dev/null')
call('add-apt-repository -y ppa:webupd8team/java > /dev/null')

call('apt-get update > /dev/null')
install('oracle-java%s-installer > /dev/null' % json_data['version'])

append('/etc/environment', '''
JAVA_HOME=%(dir)s
JRE_HOME=%(dir)s/jre
JDK_HOME=%(dir)s
''' % {'dir': '/usr/lib/jvm/java-%s-oracle' % json_data['version']})

call('java -version')
