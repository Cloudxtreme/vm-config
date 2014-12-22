from util import *

json_data = load_config()

if json_data['run-scripts']:
    for script in json_data['run-scripts']:
        call(script)
