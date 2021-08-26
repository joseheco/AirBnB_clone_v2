#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

sudo apt-get update
# Install Nginx if it not already installed
sudo apt-get -y install nginx
sudo service nginx start
# Create the folder if not exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
# create a fake HTML file
touch data/web_static/releases/test/index.html
sudo echo "Hello airbnb HTML fake" | sudo tee /data/web_static/releases/test/index.html
# Create a symbolic link 
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group
sudo chown -hR ubuntu:ubuntu /data/
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart

