#!/bin/bash

# Docker Test Script
echo "🐳 Testing Dockerized Markdown to DOCX Converter"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Build
echo "📦 Step 1: Building Docker image..."
if docker compose build; then
    echo -e "${GREEN}✅ Build successful${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi
echo ""

# Test 2: Start
echo "🚀 Step 2: Starting container..."
if docker compose up -d; then
    echo -e "${GREEN}✅ Container started${NC}"
else
    echo -e "${RED}❌ Failed to start container${NC}"
    exit 1
fi
echo ""

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 5
echo ""

# Test 3: Check status
echo "📊 Step 3: Checking container status..."
docker compose ps
echo ""

# Test 4: Health check
echo "🏥 Step 4: Health check..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    echo "Response: $HEALTH_RESPONSE"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "Response: $HEALTH_RESPONSE"
    docker compose logs backend
    exit 1
fi
echo ""

# Test 5: API root
echo "📡 Step 5: Testing API root endpoint..."
ROOT_RESPONSE=$(curl -s http://localhost:8000/)
if [ -n "$ROOT_RESPONSE" ]; then
    echo -e "${GREEN}✅ API root accessible${NC}"
else
    echo -e "${RED}❌ API root failed${NC}"
    exit 1
fi
echo ""

# Test 6: Convert text with LaTeX
echo "🧪 Step 6: Testing conversion with LaTeX formulas..."
cat > /tmp/test_payload.json << 'EOF'
{
  "markdown_content": "# Test Document\n\n## LaTeX Formulas\n\nInline formula: \\( x^2 + y^2 = r^2 \\)\n\nBlock formula:\n\\[\n\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\n\\]\n\nLegacy notation: ( E = mc^2 )\n\nTable test:\n\n| Type | Formula |\n|------|--------|\n| Quadratic | ( B^2 - 4AC < 0 ) |"
}
EOF

CONVERT_RESPONSE=$(curl -s -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d @/tmp/test_payload.json)

if echo "$CONVERT_RESPONSE" | grep -q "download_url"; then
    echo -e "${GREEN}✅ Conversion successful${NC}"
    DOWNLOAD_URL=$(echo "$CONVERT_RESPONSE" | grep -o '"download_url":"[^"]*"' | cut -d'"' -f4)
    echo "Download URL: $DOWNLOAD_URL"
    
    # Test 7: Download file
    echo ""
    echo "📥 Step 7: Testing file download..."
    if curl -s -o /tmp/test_output.docx "http://localhost:8000$DOWNLOAD_URL"; then
        if [ -f /tmp/test_output.docx ] && [ -s /tmp/test_output.docx ]; then
            FILE_SIZE=$(stat -f%z /tmp/test_output.docx 2>/dev/null || stat -c%s /tmp/test_output.docx)
            echo -e "${GREEN}✅ File downloaded successfully (${FILE_SIZE} bytes)${NC}"
        else
            echo -e "${RED}❌ Downloaded file is empty${NC}"
        fi
    else
        echo -e "${RED}❌ Download failed${NC}"
    fi
else
    echo -e "${RED}❌ Conversion failed${NC}"
    echo "Response: $CONVERT_RESPONSE"
    docker compose logs backend
    exit 1
fi
echo ""

# Test 8: View logs
echo "📋 Step 8: Container logs (last 20 lines)..."
docker compose logs --tail=20 backend
echo ""

# Summary
echo "=================================================="
echo -e "${GREEN}🎉 All tests passed!${NC}"
echo ""
echo "Container is running and ready for deployment!"
echo ""
echo "Useful commands:"
echo "  - View logs: docker compose logs -f backend"
echo "  - Stop: docker compose down"
echo "  - Restart: docker compose restart"
echo ""
echo -e "${YELLOW}To stop the container, run: docker compose down${NC}"
