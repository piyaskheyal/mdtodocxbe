# Quick Docker Deployment Guide

## 🚀 Quick Start

### Build and Run
```bash
# Build the image
docker compose build

# Start the container
docker compose up -d

# Check logs
docker compose logs -f backend

# Check health
curl http://localhost:8000/health
```

### Test the API
```bash
# Simple health check
curl http://localhost:8000/health

# Test conversion (note: field is "markdown" not "markdown_content")
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello World\n\nTest formula: \\( x^2 + y^2 = r^2 \\)"}'
```

### Stop
```bash
docker compose down
```

## 📦 Deploy to VPS

### 1. Copy files to VPS
```bash
# Using rsync (from your local machine)
rsync -avz --exclude='.venv' --exclude='__pycache__' \
  /home/kheyal/dev/mdtodocxbe/ user@YOUR_VPS_IP:~/mdtodocxbe/

# Or using git (on VPS)
git clone YOUR_REPO_URL
cd mdtodocxbe
```

### 2. On VPS - Install Docker
```bash
# Update and install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (optional, to avoid sudo)
sudo usermod -aG docker $USER
# Then logout and login again
```

### 3. Build and Run on VPS
```bash
cd ~/mdtodocxbe

# Build and start
docker compose up -d --build

# Check logs
docker compose logs -f backend

# Test it
curl http://localhost:8000/health
```

### 4. Access from outside VPS
Your API will be available at: `http://YOUR_VPS_IP:8000`

Make sure port 8000 is open in your firewall:
```bash
# Ubuntu/Debian with UFW
sudo ufw allow 8000/tcp
sudo ufw reload
```

Test from your local machine:
```bash
curl http://YOUR_VPS_IP:8000/health
```

## 🔧 Useful Commands

```bash
# View logs
docker compose logs -f backend

# Restart
docker compose restart backend

# Stop
docker compose down

# Rebuild and restart
docker compose up -d --build

# Check status
docker compose ps

# Access container shell
docker compose exec backend bash

# Check Pandoc version inside container
docker compose exec backend pandoc --version
```

## 🔍 Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs backend

# Check if port is in use
sudo netstat -tulpn | grep 8000
```

### Pandoc not found
```bash
# Access container and check
docker compose exec backend bash
pandoc --version
```

### 422 Error on /convert/text
Make sure your request has the correct format:
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Title\n\nContent here"}'
```

The JSON must have `markdown` field (not `markdown_content` or `content`).

### Permission issues
```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 backend/uploads
```

## 📊 Using Nginx Reverse Proxy (Optional)

If you want to use a standard port (80) instead of 8000:

```bash
# Install nginx
sudo apt-get install nginx

# Create config
sudo nano /etc/nginx/sites-available/mdtodocx
```

Add:
```nginx
server {
    listen 80;
    server_name YOUR_VPS_IP;
    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/mdtodocx /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Then update docker compose.yml to only listen on localhost:
```yaml
    ports:
      - "127.0.0.1:8000:8000"
```

Now your API is accessible at `http://YOUR_VPS_IP` (port 80).

## 🎯 Quick Reference

| Command | Description |
|---------|-------------|
| `docker compose up -d` | Start container |
| `docker compose down` | Stop container |
| `docker compose logs -f` | View logs |
| `docker compose ps` | Check status |
| `docker compose restart` | Restart |
| `docker compose exec backend bash` | Shell access |
