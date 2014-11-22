from util import *

call('apt-get -qy install maven')
append('/etc/environment', 'MAVEN_HOME="/usr/share/maven"\n')

