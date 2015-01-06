from util import *
import os

json_data = load_config()['git-project']

call('[ ! -d \"%(dir)s\" ] && mkdir -p %(dir)s' % {'dir': json_data['dir']})
os.chdir(json_data['dir'])

call('git clone %s .' % json_data['origin'])
call('git checkout %s' % json_data['branch'] if 'branch' in json_data else 'master')

