from util import *

config = load_config()
json_data = config['magento'] if 'magento' in config else dict()

mysql_user = config['mysql']['user'] if 'user' in config['mysql'] else 'root'
mysql_pass = config['mysql']['password'] if 'password' in config['mysql'] else config['mysql']['root_password']

version = json_data['version'] if 'version' in json_data else '1.9.1.1'
data_version = json_data['data_version'] if 'data_version' in json_data else '1.9.1.0'
sample = json_data['sample'] if 'sample' in json_data else True
db_name = json_data['db'] if 'db' in json_data else 'magento'

locale = json_data['locale'] if 'locale' in json_data else 'en_US'
timezone = json_data['timezone'] if 'timezone' in json_data else 'America/Los_Angeles'
use_rewrites = json_data['use_rewrites'] if 'use_rewrites' in json_data else True
currency = json_data['currency'] if 'currency' in json_data else 'USD'

admin_email = json_data['admin_email'] if 'admin_email' in json_data else 'admin@example.com'
admin_name = json_data['admin_name'] if 'admin_name' in json_data else 'admin'
admin_pass = json_data['admin_pass'] if 'admin_pass' in json_data else '1qazxsw23edc'
admin_last_name = json_data['admin_last_name'] if 'admin_last_name' in json_data else 'Doe'
admin_first_name = json_data['admin_first_name'] if 'admin_first_name' in json_data else 'John'

port = [p['host'] for p in config['vm']['forwarding'] if p['guest'] == 80][0]

call('rm -rf /var/www/html/*')

file_name = 'magento-%s.tar.gz' % version
if is_file_exists(file_name):
    wget('http://www.magentocommerce.com/downloads/assets/%s/%s' % (version, file_name))

extract_tar('tar -zxvf %s' % file_name)

call('mv magento/* magento/.htaccess /var/www/html/')
call('chmod -R o+w /var/www/html/media /var/www/html/var')
call('chmod o+w /var/www/html/app/etc')

# Create db
call('mysql -u%s -p%s -e "create database %s"' % (mysql_user, mysql_pass, db_name))

if sample:
    file_name = 'magento-sample-data-%s.tar.gz' % data_version

    if is_file_exists(file_name):
        wget('http://www.magentocommerce.com/downloads/assets/%s/%s' % (data_version, file_name))

    extract_tar(file_name)
    copy('magento-sample-data-%s/skin/*' % data_version, 'httpdocs/skin/')
    copy('magento-sample-data-%s/media/*' % data_version, 'httpdocs/media/')
    call('mysql -u root %(db)s < magento-sample-data-%(v)s/magento_sample_data_for_%(v)s.sql' % {
        'db': db_name,
        'v': data_version
    })

# Run installer
call("""
cd /vagrant/www/html
sudo /usr/bin/php -f install.php -- --license_agreement_accepted yes \\
    --locale %(locale)s --timezone "%(timezone)s" --default_currency %(currency)s \\
    --db_host localhost --db_name %(db)s --db_user %(mysql_user)s --db_pass %(mysql_pass)s \\
    --url "http://127.0.0.1:%(port)s/" --use_rewrites %(rewrites)s \\
    --use_secure no --secure_base_url "http://127.0.0.1:%(port)s/" --use_secure_admin no \\
    --skip_url_validation yes \\
    --admin_lastname %(admin_last_name)s --admin_firstname %(admin_first_name)s --admin_email "%(admin_email)s" \\
    --admin_username %(admin_name)s --admin_password %(admin_pass)s
/usr/bin/php -f shell/indexer.php reindexall
""" % {
    'db': db_name,
    'locale': locale,
    'timezone': timezone,
    'port': port,
    'rewrites': 'yes' if use_rewrites else 'no',
    'currency': currency,
    'admin_email': admin_email,
    'admin_name': admin_name,
    'admin_pass': admin_pass,
    'admin_last_name': admin_last_name,
    'admin_first_name': admin_first_name,
    'mysql_user': mysql_user,
    'mysql_pass': mysql_pass
})

wget('https://raw.github.com/netz98/n98-magerun/master/n98-magerun.phar')
call('chmod +x ./n98-magerun.phar')
call('mv ./n98-magerun.phar /usr/local/bin/')
