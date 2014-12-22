from util import *

json_data = load_config()

# Provision
if json_data['provision-scripts']:
    for script in json_data['provision-scripts']:
        call(script)

# Add cron tab
if json_data['cron-records']:
    call('python scripts/cron.py')

# Execution init
if json_data['run-scripts']:
    for script in json_data['run-scripts']:
        call(script)