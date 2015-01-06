from util import *

json_data = load_config()['grails']

command = 'echo "source /root/.gvm/bin/gvm-init.sh; %s" | bash'
call(command % 'gvm install grails %s' % json_data['version'])