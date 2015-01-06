from scripts.util import *

json_data = load_config()

# Provision
if 'provision-scripts' in json_data:
    for script in json_data['provision-scripts']:
        call(script)

# Add cron tab
if 'cron-records' in json_data:
    call('python scripts/cron.py')

# Execution init
if 'run-scripts' in json_data:
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
