from scripts.util import *

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

# Register auto load
with open('/etc/init/vm-config.conf', 'w+') as conf_file:
    conf_file.write("""description     "VM-Config: Start up execution"

start on runlevel [2345]
stop on starting rc RUNLEVEL=[016]

respawn
exec python %(root)srun.py
    """ % {'root': root_dir})