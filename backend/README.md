# Markdown to DOCX Converter - Backend API

FastAPI backend service that converts Markdown files to DOCX format using Pandoc.

## Features

- ✅ Convert markdown text (paste) to DOCX
- ✅ Upload markdown files and convert to DOCX
- ✅ Download converted DOCX files
- ✅ CORS enabled for frontend integration
- ✅ Error handling for invalid markdown or missing Pandoc
- ✅ File cleanup endpoint

## Prerequisites

### 1. Pandoc Installation

This backend requires **Pandoc** to be installed on your system.

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install pandoc
```

**macOS:**
```bash
brew install pandoc
```

**Windows:**
Download from [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

Verify installation:
```bash
pandoc --version
```

### 2. Python 3.8+

Ensure Python 3.8 or higher is installed:
```bash
python3 --version
```

## Installation

1. **Clone or navigate to the backend directory:**
```bash
cd backend
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Server

**Development mode:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
python main.py
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns API information and available endpoints.

### 2. Health Check
```
GET /health
```
Returns server health status and Pandoc installation status.

**Response:**
```json
{
  "status": "healthy",
  "pandoc_installed": true
}
```

### 3. Convert Text to DOCX
```
POST /convert/text
```

**Request Body:**
```json
{
  "markdown": "# Hello World\n\nThis is **markdown** text.",
  "filename": "my-document"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversion successful",
  "download_url": "/download/my-document_a1b2c3d4.docx",
  "filename": "my-document_a1b2c3d4.docx"
}
```

### 4. Upload and Convert File
```
POST /convert/upload
```

**Form Data:**
- `file`: Markdown file (.md)

**Response:**
```json
{
  "success": true,
  "message": "Conversion successful",
  "download_url": "/download/document_a1b2c3d4.docx",
  "filename": "document_a1b2c3d4.docx"
}
```

### 5. Download Converted File
```
GET /download/{filename}
```

Downloads the converted DOCX file.

### 6. Cleanup Files
```
DELETE /cleanup/{filename}
```

Deletes both the markdown and DOCX files for a given base filename.

## Directory Structure

```
backend/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── uploads/               # Storage directory
    ├── md/                # Markdown files
    └── docx/              # Converted DOCX files
```

## Testing the API

### Using cURL

**Test text conversion:**
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Test\n\nThis is a **test** document."}'
```

**Test file upload:**
```bash
curl -X POST http://localhost:8000/convert/upload \
  -F "file=@test.md"
```

**Download file:**
```bash
curl -O http://localhost:8000/download/converted_a1b2c3d4.docx
```

### Using Python requests

```python
import requests

# Convert text
response = requests.post(
    "http://localhost:8000/convert/text",
    json={
        "markdown": "# Hello\n\nThis is **markdown**.",
        "filename": "test"
    }
)
result = response.json()
print(result)

# Download file
download_url = result["download_url"]
file_response = requests.get(f"http://localhost:8000{download_url}")
with open("output.docx", "wb") as f:
    f.write(file_response.content)
```

## Error Handling

The API returns appropriate HTTP status codes:

- **400 Bad Request:** Invalid input (empty markdown, wrong file type)
- **404 Not Found:** File not found
- **500 Internal Server Error:** Pandoc not installed or conversion failed

## CORS Configuration

CORS is enabled for common localhost ports:
- http://localhost:3000
- http://localhost:5173
- http://localhost:8080
- http://127.0.0.1:3000
- http://127.0.0.1:5173
- http://127.0.0.1:8080

To add more origins, edit the `allow_origins` list in `main.py`.

## Notes

- Files are stored with unique IDs to prevent conflicts
- Markdown files support tables, formulas (KaTeX/LaTeX), code blocks, and more
- Temporary files are stored in the `uploads/` directory
- Use the cleanup endpoint to remove old files

## Troubleshooting

**"Pandoc is not installed" error:**
- Install Pandoc using the instructions above
- Ensure Pandoc is in your system PATH
- Restart the server after installing Pandoc

**File not found error:**
- Check that the `uploads/md/` and `uploads/docx/` directories exist
- Ensure the application has write permissions

## License

MIT
