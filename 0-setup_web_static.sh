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

rm /data/web_static/current || true;
ln -sf /data/web_static/releases/test/ /data/web_static/current;

chown -R ubuntu:ubuntu /data/;

# Variables to put the location alias
index_tester="\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}";
file_to_update="/etc/nginx/sites-enabled/default";

# Checks if /etc/nginx/sites-enabled/default exists and updates it if so.
if [ -f /etc/nginx/sites-enabled/default ]; then
	grep "location /hbnb_static/ {" -q "${file_to_update}" || sed -i "/^\tserver_name;/a\ ${index_tester}" "${file_to_update}";
fi


service nginx status >> /dev/null || service nginx start;
service nginx restart;
