from util import *

call('apt-get -qy install nginx')

static_config = """
server {
    listen   80; ## listen for ipv4
    listen   [::]:80; ## listen for ipv6

    server_name static.yourdomain.com;

    access_log /var/log/nginx/cdn.access.log;
    error_log  /var/log/nginx/cdn.error.log;

    root /var/www/;

    location ~ /\. { deny all; }
    location ~ ~$ { deny all; }
    location ~ \.(php|jsp|jspx|asp|aspx)$ { deny all; }
}
"""

call('/etc/init.d/nginx stop')

with open('/etc/nginx/sites-available/static', 'w+') as conf_file:
    conf_file.write(static_config)

call('rm -f /etc/nginx/sites-enabled/*')

call('ln -s /etc/nginx/sites-available/static /etc/nginx/sites-enabled/static')

call('/etc/init.d/nginx start')

echo('Please configure your static at /etn/nginx/sites-enabled/static.')
