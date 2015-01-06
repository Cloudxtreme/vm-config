from util import *

json_data = load_config()

if json_data['cron-records']:
    for record in json_data['cron-records']:
        append('/etc/crontab', record + '\n')

call('/etc/init.d/cron restart')