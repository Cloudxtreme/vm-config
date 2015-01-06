from util import *

json_data = load_config()['elasticsearch']

location = 'https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-%s.deb'
output_file = 'elasticsearch.deb'

url = location % json_data['version']

call('wget %s -O %s' % (url, output_file))
call('dpkg -i %s' % output_file)

call('update-rc.d elasticsearch defaults 95 10')
call('/etc/init.d/elasticsearch start')

call('/etc/init.d/elasticsearch status')
call('curl -XGET "http://localhost:9200/_cluster/health?pretty=true"')