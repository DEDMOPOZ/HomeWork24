# Run Project using Docker
docker-compose build
docker-compose run backend python src/manage.py migrate
docker-compose up

# Run Gunicorn
gunicorn -w 4 -b unix:/tmp/gunicorn.sock --chdir src core.wsgi --timeout 60 --log-level debug --max-requests 10000

# NGinx Config
worker_processes  1;
error_log  /var/log/nginx/error.log;
worker_rlimit_nofile 8192;

events {
  worker_connections  1024;  ## Default: 1024
}

http {
  include    /etc/nginx/mime.types;
  include    /etc/nginx/proxy.conf;
  include    /etc/nginx/fastcgi.conf;
  index    index.html index.htm index.php;
  
  log_format   main '$remote_addr - $remote_user [$time_local]  $status '
    '"$request" $body_bytes_sent "$http_referer" '
    '"$http_user_agent" "$http_x_forwarded_for"';
  access_log   /var/log/nginx/access.log  main;

  server_names_hash_bucket_size 128; # this seems to be required for some vhosts
  
  upstream django {
    server unix:/tmp/gunicorn.sock fail_timeout=0;
  }

  server {
    listen 80;
    listen [::]:80;
    server_name 127.0.0.1 blog.com www.blog.com;

    location = /favicon.icon { access_log off; log_not_found off; }
    
    location /static/ {
    	root /home/dedmopoz/python/HomeWork18/static_content;
    }
    
    location / {
    	proxy_pass http://django;
    }
  }
}
