from util import *

call('echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections')
call('echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections')

call('apt-get -qy remove openjdk*')
call('add-apt-repository -y ppa:webupd8team/java')

call('apt-get -qy update')
call('apt-get -qy install oracle-java8-installer')

append('/etc/environment', 'JAVA_HOME="/usr/lib/jvm/java-8-oracle"\n')
append('/etc/environment', 'JRE_HOME="/usr/lib/jvm/java-8-oracle/jre"\n')
append('/etc/environment', 'JDK_HOME="/usr/lib/jvm/java-8-oracle/"\n')

