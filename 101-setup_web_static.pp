#Make the tsk 0 under puppet
exec {'apt-get -y update' : }
-> exec {'apt-get -y install nginx' : }
-> exec {'mkdir -p /data/web_static/releases/test' : }
-> exec {'mkdir -p /data/web_static/shared' : }
-> exec {'echo "Hello world" > /data/web_static/releases/test/index.html' : }
-> exec {'ln -sf /data/web_static/releases/test/ /data/web_static/current' : }
-> exec {'chown -hR ubuntu:ubuntu /data/' : }
-> exec {'sed -i "38i\\\tlocation /hbnb_static/ {\n\t\t alias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default' : }
-> exec {'service nginx restart' : }
