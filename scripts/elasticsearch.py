from util import *

json_date = load_config()

location = 'https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-%s.deb'
output_file = 'elasticsearch.deb'

url = location % json_date['elasticsearch']['version']

call('wget %s -O %s' % (url, output_file))
call('dpkg -i %s' % output_file)

call('update-rc.d elasticsearch defaults 95 10')
call('/etc/init.d/elasticsearch start')

call('/etc/init.d/elasticsearch status')
call('curl -XGET "http://localhost:9200/_cluster/health?pretty=true"')