#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static
# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
# Create a fake HTML file
sudo echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
 </html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link /data/web_static/current
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart Nginx to apply changes
sudo service nginx restart
