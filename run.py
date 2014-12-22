import json
import os

json_data = open('config.json')
config = json.load(json_data)
json_data.close()

if json_data['run-scripts']:
    for script in json_data['run-scripts']:
        os.system(script)
