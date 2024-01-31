# Install Nginx
class nginx {
  package { 'nginx':
    ensure => installed,
  }
}

# Configure Nginx for serving web_static content
class web_static_nginx {
  file { '/etc/nginx/sites-available/default':
    ensure => file,
    content => "
server {
    listen 80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location / {
        try_files $uri $uri/ =404;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
        internal;
    }

    add_header X-Served-By $hostname;
}
",
    notify => Service['nginx'],
  }

  file { '/etc/nginx/sites-enabled/default':
    ensure => link,
    target => '/etc/nginx/sites-available/default',
    notify => Service['nginx'],
  }
}

# Create web_static directories and a sample HTML file
class web_static {
  file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
    ensure => directory,
  }

  file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
",
  }
}

# Include the defined classes
include nginx
include web_static
include web_static_nginx
