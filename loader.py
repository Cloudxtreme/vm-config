import urllib
import json
import os
import os.path

script_dir = 'scripts'

if not os.path.exists(script_dir):
    os.mkdir(script_dir, 0755)

base_url = 'https://raw.githubusercontent.com/aiskov/vm-config/develop'

print """
Downloading sample configuration file
"""
urllib.urlretrieve("%s/config.json" % base_url, "config-sample.json")

print """
Downloading script files
"""
url = "https://api.github.com/repositories/25528321/contents/scripts?ref=develop"
files = json.loads(urllib.urlopen(url).read())

for file in files:
    print 'Downloding - %s' % file['path']
    urllib.urlretrieve(file['download_url'], file['path'])

print '%s files downloaded' % len(files)
print 'Preparation done'
