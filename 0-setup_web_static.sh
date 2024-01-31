#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
 </html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_content="
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
        internal;
    }

    add_header X-Served-By $HOSTNAME;
}
"

echo "$config_content" | sudo tee /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart
