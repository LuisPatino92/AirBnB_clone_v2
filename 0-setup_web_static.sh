#!/usr/bin/env bash
# This script sets everything up to serve AirBnB content.

# Install Nginx if it is not installed

if ! [ -x "$(command -v nginx)" ]
then

	apt-get update -y;
	apt-get upgrade -y;
	apt-get install -y nginx;
fi

mkdir -p /data/web_static/releases/test/;
mkdir -p /data/web_static/shared/;

echo "<h1>FakeHTML for testing pourposes</h1>" >> /data/web_static/releases/test/index.html;

ln -sf /data/web_static/releases/test/ /data/web_static/current;

chown -R ubuntu:ubuntu /data/;

# Variables to put the location alias
index_tester="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t}";
file_to_update="/etc/nginx/sites-enabled/default";

# Checks if /etc/nginx/sites-enabled/default exists and updates it if so.
if [ -f /etc/nginx/sites-enabled/default ]; then
	grep "location /hbnb_static {" -q "${file_to_update}" || sed -i "/^\tserver_name _;$/a\ ${index_tester}" "${file_to_update}";
fi

# Establish a localhost server
new_server="server {\n\n\tlisten localhost:80;\n\troot /var/www/html;\n\n\tindex index.html index.htm index.nginx-debian.html;\n\n\tserver_name localhost;\n\n\tadd_header X-Served-By 2450-web-01 always;\n\n\terror_page 404 /hbnb_static/;\n\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t}\n\n\tlocation / {\n\t\ttry_files $uri $uri/ =404;\n\t}\n}";

grep "listen localhost:80" -q "${file_to_update}" || echo -e "${new_server}" >> "${file_to_update}";

service nginx status >> /dev/null || service nginx start;
nginx -s reload;
