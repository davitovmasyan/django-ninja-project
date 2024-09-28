# Initial deployment instructions

## SSH into the server
```bash
ssh -i <path-to-pem-file> ubuntu@<server-ip>
```

## Update the server
```bash
sudo apt-get update
sudo apt-get upgrade
```

## Install Docker
```bash
sudo apt-get install docker.io
```

## Add the user to the docker group
```bash
sudo usermod -aG docker $USER
```

## Enable monitoring tools
```bash
docker plugin install grafana/loki-docker-driver:2.9.2 --alias loki --grant-all-permissions
docker run -d --net host --name loki grafana/loki
docker run -d --net host --name grafana grafana/grafana
```

## Reconnect to the server

## Install nginx
```bash
sudo apt-get install nginx
```

## Install certbot
```bash
sudo apt-get install certbot python3-certbot-nginx
```

### Create a directory for the api
```bash
sudo mkdir /var/www/api
```

### Change permissions
```bash
sudo chown -R $USER:$USER /var/www/api
```

## Add nginx configuration
```bash
sudo nano /etc/nginx/sites-available/api.conf
```

```nginx
server {
    listen 80;
    server_name api.django-ninja-project;
    
    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/api;
    }

    location /media/ {
        autoindex off;
        root /var/www/api;
    }

    location = /robots.txt {
	    alias /var/www/api/collectstatic/robots.txt;
    }

    location / {
	proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        client_max_body_size 100M;
    }

    error_log /var/log/nginx/api.django-ninja-project_error.log;
    access_log /var/log/nginx/api.django-ninja-project_access.log;
}
```

## Create symbolic link
```bash
sudo ln -s /etc/nginx/sites-available/api.conf /etc/nginx/sites-enabled/
```

## Test the configuration
```bash
sudo nginx -t
```

## Restart nginx
```bash
sudo systemctl restart nginx
```

## Install certbot certificate
```bash
sudo certbot --nginx
```

## Run github workflow

## Create superuser
```bash
docker exec -it <container-id> ./manage.py createsuperuser
```
