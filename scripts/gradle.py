from util import *

json_data = load_config()['gradle']

command = 'echo "source /root/.gvm/bin/gvm-init.sh; %s" | bash'
call(command % 'gvm install gradle %s' % json_data['version'])
