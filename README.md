# Trump Social Scraper

FastAPI backend that scrapes Truth Social posts and provides a live API + Server-Sent Events (SSE) stream.  
Deployed with Docker, PostgreSQL, and secured with SSL certificates.

GitHub: [https://github.com/DoableDanny/trump-social-scraper](https://github.com/DoableDanny/trump-social-scraper)

---

## 🚀 Setup Instructions (Development)

1. **Clone the repository:**

```bash
git clone https://github.com/DoableDanny/trump-social-scraper.git
cd trump-social-scraper
```

2. **Start backend and database (dev mode):**

```bash
docker compose -f docker-compose.dev.yml up --build
```

3. **Useful Commands:**

| Action                      | Command                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Stop and remove all         | `docker compose down -v`                                                             |
| Freeze Python packages      | `pip freeze > requirements.txt`                                                      |
| Connect to Postgres locally | `psql -h 127.0.0.1 -p 5433 -U postgres`                                              |
| Connect inside Docker db    | `docker exec -it trump-social-scraper-db-1 psql -U postgres -d trump_social_scraper` |

---

4.  **Start frontend (dev mode):**

`yarn dev`

## 🛠️ API Documentation

Base URL:

```
https://trump-api.188.166.149.237.nip.io/
```

| Method | Endpoint  | Description                                  |
| ------ | --------- | -------------------------------------------- |
| GET    | `/`       | Basic health check                           |
| GET    | `/truths` | Get latest scraped truths with AI summaries  |
| GET    | `/stream` | Server-Sent Events (SSE) for live new truths |

---

## 🐳 Deployment Notes (Production)

### First time setup:

1. **SSH into your server**
2. **Clone the repo if not done already:**

```bash
git clone https://github.com/DoableDanny/trump-social-scraper.git
cd trump-social-scraper
```

3. **Make the deploy script executable:**

```bash
chmod +x deploy.sh
```

4. **Setup SSL manually (see below)**

5. **Start everything:**

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

---

6. **Deploy frontend**

React frontend can be deployed to Netlify.

### 🔥 Redeploying updates (Zero Downtime)

Whenever you push new updates to GitHub:

1. SSH into your server
2. Check `git status`. If there are any tracked file changes on server, `git restore <file_name>` to get make them same as remote, so can safely `git pull` without merge conflicts (untracked server files are fine).
3. Run the deploy script:

```bash
./deploy.sh
```

This:

- Pulls latest Git changes
- Rebuilds backend image
- Restarts backend container only
- Leaves database and SSL certificates untouched

---

## 🔒 SSL Certificate Setup (One-Time Only)

> These steps were needed to issue HTTPS certificates for Nginx + Certbot.

---

### 1. Setup `nginx/prod.conf` for HTTP only (no SSL yet)

```nginx
server {
    listen 80;
    server_name trump-api.188.166.149.237.nip.io;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 2. Start Docker services without SSL yet:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

---

### 3. Issue SSL cert using Certbot:

```bash
docker compose -f docker-compose.prod.yml run --rm certbot   certonly   --webroot   --webroot-path=/var/www/certbot   --email your@email.com   --agree-tos   --no-eff-email   -d trump-api.188.166.149.237.nip.io
```

✅ If success, your certs will be available inside `/nginx/certbot/conf/...`

---

### 4. Update `nginx/prod.conf` to enable HTTPS

Replace your nginx config with this:

```nginx
server {
    listen 80;
    server_name trump-api.188.166.149.237.nip.io;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name trump-api.188.166.149.237.nip.io;

    ssl_certificate /etc/letsencrypt/live/trump-api.188.166.149.237.nip.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/trump-api.188.166.149.237.nip.io/privkey.pem;

    location / {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 5. Restart containers

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d
```

✅ Now HTTPS is working!

Access your API at:  
[https://trump-api.188.166.149.237.nip.io](https://trump-api.188.166.149.237.nip.io)

---

Built by Dan Adams — April 2025.
