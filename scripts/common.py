from util import *

json_data = load_config()

call('dpkg-reconfigure tzdata')
call('echo "%s" > /etc/timezone' % json_data['location'])
call('dpkg-reconfigure -f noninteractive tzdata')

call('date && more /etc/timezone')

call('export LANGUAGE="%s"' % json_data['locale'])
call('echo \'LANGUAGE="%s"\' >> /etc/default/locale' % json_data['locale'])
call('echo \'LC_ALL="%s"\' >> /etc/default/locale' % json_data['locale'])

call('locale-gen %s' % json_data['locale'])
call('dpkg-reconfigure locales')

call('locale')

pkgs = ('nano', 'links', 'wget', 'openssl', 'git', 'tree', 'curl', 'python-pip')
apt_get(pkgs)
