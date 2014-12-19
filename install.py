import urllib
import json
import os

script_dir = 'scripts'
os.mkdir('scripts', 0755)
base_url = 'https://raw.githubusercontent.com/aiskov/vm-config/develop'

"""
Downloading sample configuration file
"""
urllib.urlretrieve("%s/config.json" % base_url, "config-sample.json")

url = "https://api.github.com/repositories/aiskov/contents/scripts?ref=develop"

"""
Downloading script files
"""
for file in json.loads(urllib.urlopen(url).read()):
    print 'Downloding - %s' % file['path']
    urllib.urlretrieve(file['download_url'], file['path'])

print 'Preparation done'
