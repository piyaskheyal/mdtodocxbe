# Docker Deployment Guide

## 📋 Prerequisites

- Docker installed on your VPS
- Docker Compose installed
- Port 8000 available (or modify in docker compose.yml)

## 🧪 Testing Locally

### 1. Build the Docker image
```bash
docker compose build
```

### 2. Start the container
```bash
docker compose up -d
```

### 3. Check if it's running
```bash
docker compose ps
```

### 4. View logs
```bash
docker compose logs -f backend
```

### 5. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Test conversion (text)
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown_content": "# Test\n\nThis is a test with formula \\( x = y \\)."}'

# Full test with download
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown_content": "# Hello\n\nFormula: ( x^2 + y^2 = r^2 )"}' \
  | jq -r '.download_url' \
  | xargs -I {} curl -O http://localhost:8000{}
```

### 6. Stop the container
```bash
docker compose down
```

## 🚀 Deploying to VPS

### Step 1: Prepare your VPS

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Install Docker (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y docker.io docker compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional, to avoid sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

### Step 2: Upload your project

**Option A: Using Git (Recommended)**
```bash
# On VPS
cd ~
git clone https://github.com/yourusername/mdtodocxbe.git
cd mdtodocxbe
```

**Option B: Using SCP**
```bash
# From your local machine
scp -r /home/kheyal/dev/mdtodocxbe user@your-vps-ip:~/
```

**Option C: Using rsync**
```bash
# From your local machine
rsync -avz --exclude='.venv' --exclude='__pycache__' \
  /home/kheyal/dev/mdtodocxbe/ user@your-vps-ip:~/mdtodocxbe/
```

### Step 3: Build and run on VPS

```bash
# SSH into VPS
ssh user@your-vps-ip

# Navigate to project
cd ~/mdtodocxbe

# Build and start
docker compose up -d --build

# Verify it's running
docker compose ps
docker compose logs -f backend
```

### Step 4: Test deployment

```bash
# From your VPS or local machine
curl http://your-vps-ip:8000/health
```

### Step 5: Configure firewall (if needed)

```bash
# Ubuntu/Debian with UFW
sudo ufw allow 8000/tcp
sudo ufw reload

# Check status
sudo ufw status
```

## 🔧 Production Configuration

### Using Nginx as Reverse Proxy (Recommended)

1. **Install Nginx**
```bash
sudo apt-get install nginx
```

2. **Create Nginx configuration**
```bash
sudo nano /etc/nginx/sites-available/mdtodocx
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your VPS IP
    
    client_max_body_size 50M;  # Allow larger file uploads

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

3. **Enable site and restart Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/mdtodocx /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. **Update docker compose.yml** (remove port mapping for security)
```yaml
    ports:
      - "127.0.0.1:8000:8000"  # Only localhost can access
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

## 📊 Useful Commands

### View logs
```bash
docker compose logs -f backend
docker compose logs --tail=100 backend
```

### Restart service
```bash
docker compose restart backend
```

### Update and redeploy
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker compose up -d --build

# Or force recreate
docker compose up -d --force-recreate --build
```

### Check resource usage
```bash
docker stats mdtodocx-backend
```

### Access container shell
```bash
docker compose exec backend bash
```

### Clean up
```bash
# Stop and remove containers
docker compose down

# Remove all (including volumes)
docker compose down -v

# Remove unused images
docker image prune -a
```

## 🔍 Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs backend

# Check if port is already in use
sudo netstat -tulpn | grep 8000
```

### Pandoc not working
```bash
# Access container and check
docker compose exec backend bash
pandoc --version
```

### Permission issues with uploads
```bash
# Fix permissions
sudo chown -R 1000:1000 backend/uploads
```

### Out of disk space
```bash
# Clean up Docker
docker system prune -a --volumes
```

## 🎯 Environment Variables (Optional)

Create `.env` file for custom configuration:

```env
# .env
PORT=8000
HOST=0.0.0.0
WORKERS=4
```

Update `docker compose.yml`:
```yaml
environment:
  - PORT=${PORT:-8000}
  - WORKERS=${WORKERS:-1}
env_file:
  - .env
```

## 🔒 Security Best Practices

1. **Use Nginx reverse proxy** (hides backend port)
2. **Enable HTTPS** with Let's Encrypt
3. **Limit upload file sizes** in Nginx config
4. **Regular updates**: `docker compose pull && docker compose up -d`
5. **Monitor logs**: Set up log rotation
6. **Firewall**: Only allow necessary ports (80, 443, 22)

## 🚦 Monitoring

### Setup basic monitoring
```bash
# Install and configure monitoring (optional)
docker run -d --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  mdtodocx-backend
```

This will auto-update your container when you push new images.

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `docker compose up -d` | Start in background |
| `docker compose down` | Stop and remove |
| `docker compose logs -f` | Follow logs |
| `docker compose ps` | Check status |
| `docker compose restart` | Restart service |
| `docker compose exec backend bash` | Access shell |

---

**Your API will be available at:**
- Local: `http://localhost:8000`
- VPS: `http://your-vps-ip:8000`
- With Nginx: `http://your-domain.com`
- With SSL: `https://your-domain.com`
