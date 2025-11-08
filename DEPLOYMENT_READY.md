# ✅ Docker Deployment Ready!

## What's Been Set Up

✅ **Dockerfile** - Uses Pandoc 3.8.2.1 from your deb_files/  
✅ **docker-compose.yml** - Orchestrates the container (updated to use `docker compose`)  
✅ **Health checks** - Container auto-restarts if unhealthy  
✅ **Volume persistence** - Uploaded files persist across restarts  
✅ **Tests passing** - All conversions working with LaTeX formulas

## 🧪 Local Testing (DONE ✅)

```bash
# Build and run
docker compose build
docker compose up -d

# Test
curl http://localhost:8000/health
# Response: {"status":"healthy","pandoc_installed":true}

# Test conversion
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Test\n\nFormula: \\( x^2 + y^2 = r^2 \\)"}'

# Stop
docker compose down
```

## 🚀 Deploy to VPS

### Method 1: Using Git (Recommended)

**On your local machine:**
```bash
cd /home/kheyal/dev/mdtodocxbe
git add .
git commit -m "Docker deployment ready"
git push
```

**On your VPS:**
```bash
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker

# Clone and deploy
git clone YOUR_REPO_URL ~/mdtodocxbe
cd ~/mdtodocxbe
docker compose up -d --build

# Open firewall
sudo ufw allow 8000/tcp
sudo ufw reload

# Check logs
docker compose logs -f backend
```

### Method 2: Using rsync/scp

**From your local machine:**
```bash
# Copy entire project to VPS
rsync -avz --exclude='.venv' --exclude='__pycache__' \
  /home/kheyal/dev/mdtodocxbe/ user@YOUR_VPS_IP:~/mdtodocxbe/
```

**On your VPS:**
```bash
# Install Docker (if not already installed)
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker

# Deploy
cd ~/mdtodocxbe
docker compose up -d --build

# Open firewall
sudo ufw allow 8000/tcp
sudo ufw reload
```

## 📡 Access Your API

Once deployed on VPS:
- **Health check**: `http://YOUR_VPS_IP:8000/health`
- **API docs**: `http://YOUR_VPS_IP:8000/docs`
- **Convert endpoint**: `http://YOUR_VPS_IP:8000/convert/text`

### Test from anywhere:
```bash
# Replace YOUR_VPS_IP with your actual VPS IP
curl http://YOUR_VPS_IP:8000/health

# Test conversion
curl -X POST http://YOUR_VPS_IP:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello from VPS\n\nMath: \\( E = mc^2 \\)"}'
```

## 🔧 Useful Commands on VPS

```bash
# View logs
docker compose logs -f backend

# Restart container
docker compose restart backend

# Stop container
docker compose down

# Update and redeploy (after git pull)
docker compose up -d --build

# Check container status
docker compose ps

# Access container shell
docker compose exec backend bash

# Check Pandoc version
docker compose exec backend pandoc --version
```

## 📊 Container Info

- **Image**: Python 3.11-slim
- **Pandoc**: 3.8.2.1 (from your .deb file)
- **Port**: 8000
- **Auto-restart**: Yes (unless-stopped)
- **Health checks**: Every 30s

## 🎯 Important Notes

1. **API Field Name**: Use `"markdown"` not `"markdown_content"` in JSON requests
2. **Port 8000**: Make sure it's open in your firewall
3. **No SSL/Domain needed**: Access via IP address is fine
4. **Uploads persist**: Files in `backend/uploads/` are mounted as volume

## 🔍 Troubleshooting

### Container won't start
```bash
docker compose logs backend
```

### Port already in use
```bash
sudo netstat -tulpn | grep 8000
# Kill the process or change port in docker-compose.yml
```

### Pandoc not working
```bash
docker compose exec backend pandoc --version
# Should show: pandoc 3.8.2.1
```

### Can't access from outside
```bash
# Make sure firewall is open
sudo ufw status
sudo ufw allow 8000/tcp
sudo ufw reload
```

## 📝 Files Created

- `Dockerfile` - Container definition with Pandoc .deb installation
- `docker-compose.yml` - Container orchestration
- `.dockerignore` - Excludes unnecessary files from build
- `DEPLOY.md` - Quick deployment guide
- `DOCKER_DEPLOYMENT.md` - Comprehensive deployment guide
- `vps-deploy.sh` - Helper script for VPS setup

---

## 🎉 You're Ready to Deploy!

Your Markdown to DOCX converter with LaTeX formula support is containerized and ready for production deployment on your VPS!

**Quick Start:**
1. Push to Git or rsync to VPS
2. Run `docker compose up -d --build` on VPS
3. Open port 8000 in firewall
4. Access at `http://YOUR_VPS_IP:8000`

That's it! 🚀
