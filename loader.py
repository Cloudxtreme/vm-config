import urllib
import json
import os
import os.path

base_url = 'https://raw.githubusercontent.com/aiskov/vm-config/develop'

print """
Downloading sample configuration file
"""
urllib.urlretrieve("%s/config.json" % base_url, "config-sample.json")

print """
Downloading script files
"""
script_dir = 'scripts'

if not os.path.exists(script_dir):
    os.mkdir(script_dir, 0755)

url = "https://api.github.com/repositories/25528321/contents/scripts?ref=develop"
files = json.loads(urllib.urlopen(url).read())

for prov_file in files:
    print 'Downloading - %s' % prov_file['path']
    urllib.urlretrieve(prov_file['download_url'], prov_file['path'])

print '%s files downloaded' % len(files)
print 'Preparation done'
