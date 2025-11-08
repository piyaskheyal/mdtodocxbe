#!/bin/bash

# Quick VPS Deployment Commands
# Copy and paste these commands one by one on your VPS

echo "🚀 VPS Deployment - Markdown to DOCX Converter"
echo "==============================================="
echo ""

# Step 1: Install Docker
echo "📦 Step 1: Installing Docker..."

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Optional: Add user to docker group (requires logout/login)
sudo usermod -aG docker $USER

echo ""
echo "✅ Docker installed!"
echo ""

# Step 2: Navigate to project (assuming you already uploaded it)
echo "📂 Step 2: Navigate to project directory"
echo "Run: cd ~/mdtodocxbe"
echo ""

# Step 3: Build and run
echo "🔨 Step 3: Build and run the container"
echo "Run these commands:"
echo "  docker compose build"
echo "  docker compose up -d"
echo ""

# Step 4: Check status
echo "🔍 Step 4: Check status"
echo "Run: docker compose ps"
echo "Run: docker compose logs -f backend"
echo ""

# Step 5: Test
echo "🧪 Step 5: Test the API"
echo "Run: curl http://localhost:8000/health"
echo ""

# Step 6: Open firewall
echo "🔥 Step 6: Open firewall for port 8000"
echo "Run: sudo ufw allow 8000/tcp"
echo "Run: sudo ufw reload"
echo ""

# Done
echo "✅ Done! Your API should be accessible at http://YOUR_VPS_IP:8000"
echo ""
echo "Test from your local machine:"
echo "  curl http://YOUR_VPS_IP:8000/health"
