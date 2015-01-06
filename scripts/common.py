from util import *

call('apt-get update > /dev/null')

json_data = load_config()

call('echo "%s" > /etc/timezone' % json_data['location'])
call('dpkg-reconfigure -f noninteractive tzdata')

call('date && more /etc/timezone')

call('export LANGUAGE="%s"' % json_data['locale'])
call('echo \'LANGUAGE="%s"\' >> /etc/default/locale' % json_data['locale'])
call('echo \'LC_ALL="%s"\' >> /etc/default/locale' % json_data['locale'])

call('locale-gen %s' % json_data['locale'])
call('dpkg-reconfigure locales')

call('locale')

install('nano', 'links', 'wget', 'unzip', 'openssl', 'git', 'tree', 'curl', 'python-dev', 'python-setuptools', 'python-pip', 'ntp', 'html2text')

call('pip install virtualenv')

call('ufw allow ssh')
call('ufw default deny incoming')
call('ufw default allow outgoing')

if 'allowed-ports' in json_data:
    for port in json_data['allowed-ports']:
        call('ufw allow %s/tcp' % port)

call('ufw --force enable')
call('ufw status')

call('fallocate -l %s /swapfile' % (json_data['swap_size'] if 'swap_size' in json_data else '2G'))
call('chmod 600 /swapfile')
call('mkswap /swapfile')
call('swapon /swapfile')
call('sh -c \'echo "/swapfile none swap sw 0 0" >> /etc/fstab\'')
