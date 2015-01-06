from util import *

json_data = load_config()['groovy']

command = 'echo "source /root/.gvm/bin/gvm-init.sh; %s" | bash'
call(command % 'gvm install groovy %s' % json_data['version'])
