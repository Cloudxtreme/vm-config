import json
import os

json_data = open('config.json')
config = json.load(json_data)
json_data.close()

# Provision
if json_data['provision-scripts']:
    for script in json_data['provision-scripts']:
        os.system(script)

# Add cron tab
if json_data['cron-records']:
    os.system('python scripts/cron.py')

# Execution init
if json_data['run-scripts']:
    for script in json_data['run-scripts']:
        os.system(script)
