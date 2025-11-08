#!/bin/bash

# Markdown to DOCX Converter - Start Script

echo "🚀 Starting Markdown to DOCX Converter Backend..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r backend/requirements.txt
fi

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ ERROR: Pandoc is not installed!"
    echo "Please install Pandoc first:"
    echo "  Ubuntu/Debian: sudo apt-get install pandoc"
    echo "  macOS: brew install pandoc"
    echo "  Windows: Download from https://pandoc.org/installing.html"
    exit 1
fi

echo "✅ Pandoc version: $(pandoc --version | head -n 1)"

# Start the server
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "💡 Press Ctrl+C to stop the server"
echo ""

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
