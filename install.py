import urllib

os.mkdir('scripts', 0755);
base_url = 'https://raw.githubusercontent.com/aiskov/vm-config/develop'

urllib.urlretrieve("%s/config.json" % base_url, "config-sample.json")

