from scripts.util import *

json_data = load_config()

call('echo 1 > /vagrant/tts')

if json_data['run-scripts']:
    for script in json_data['run-scripts']:
        call(script)
