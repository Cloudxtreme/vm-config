from util import *

call('apt-get -qy install nginx')

balancer_config = """
server {
    location / {
        proxy_pass http://balancer;
        proxy_redirect          off;
        proxy_next_upstream     error timeout;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

upstream balancer {
    server backend1.example.com;
    server backend2.example.com;
}
"""

cdn_config = """
server {
    listen   80; ## listen for ipv4
    listen   [::]:80; ## listen for ipv6

    server_name cdn.yourdomain.com;

    access_log /var/log/nginx/cdn.access.log;
    error_log  /var/log/nginx/cdn.error.log;

    root /var/www/;

    location ~ /\. { deny all; }
    location ~ ~$ { deny all; }
    location ~ \.(php|jsp|jspx|asp|aspx)$ { deny all; }

    # Keep images and CSS and other static files around in browser cache for as long as possible,
    location ~* .(svg|eot|ttf|css|js|jpg|jpeg|gif|png|ico|rtf|html|txt|htm)$ {
        expires max;
        log_not_found off;
        access_log off;

        add_header Cache-Control public;

        fastcgi_hide_header Set-Cookie;

        # CORS config
        set $cors "true";

        # Determine the HTTP request method used
        if ($request_method = 'OPTIONS') {
            set $cors "${cors}options";
        }

        if ($request_method = 'GET') {
            set $cors "${cors}get";
        }

        if ($request_method = 'POST') {
            set $cors "${cors}post";
        }

        if ($cors = "true") {
            add_header 'Access-Control-Allow-Origin' '*';
        }

        if ($cors = "trueget") {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }

        if ($cors = "trueoptions") {
            add_header 'Access-Control-Allow-Origin' '*';

            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';

            # Custom headers and headers various browsers *should* be OK with but aren't
            add_header 'Access-Control-Allow-Headers' 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';

            # Tell client that this pre-flight info is valid for 20 days
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        if ($cors = "truepost") {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }
    }
}
"""

call('/etc/init.d/nginx stop')

with open('/etc/nginx/sites-available/balancer', 'w+') as conf_file:
    conf_file.write(balancer_config)

with open('/etc/nginx/sites-available/cdn', 'w+') as conf_file:
    conf_file.write(cdn_config)

call('rm -f /etc/nginx/sites-enabled/*')

call('ln -s /etc/nginx/sites-available/balancer /etc/nginx/sites-enabled/balancer')
call('ln -s /etc/nginx/sites-available/cdn /etc/nginx/sites-enabled/cdn')

call('/etc/init.d/nginx start')

echo('Please configure your balancer at /etn/nginx/sites-enabled/balancer.')
echo('Please configure your cdn at /etn/nginx/sites-enabled/cdn.')