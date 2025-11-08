"""
Markdown to DOCX Converter API - Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import check_pandoc_installed, ALLOWED_ORIGINS
from web.routes import conversion_router


# Initialize FastAPI app
app = FastAPI(
    title="Markdown to DOCX Converter API",
    description="Convert Markdown to DOCX using Pandoc with LaTeX formula support",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversion_router)


@app.on_event("startup")
async def startup_event():
    """Check if pandoc is installed on startup"""
    if not check_pandoc_installed():
        print("WARNING: Pandoc is not installed or not in PATH!")
        print("Please install pandoc: https://pandoc.org/installing.html")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Markdown to DOCX Converter API",
        "version": "2.0.0",
        "features": [
            "Convert markdown text to DOCX",
            "Upload markdown files and convert to DOCX",
            "Automatic LaTeX formula conversion",
            "Support for both inline ($formula$) and block ($$formula$$) math"
        ],
        "endpoints": {
            "POST /convert/text": "Convert markdown text to DOCX",
            "POST /convert/upload": "Upload markdown file and convert to DOCX",
            "GET /download/{filename}": "Download converted DOCX file",
            "DELETE /cleanup/{filename}": "Delete converted files",
            "GET /health": "Health check endpoint"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    pandoc_installed = check_pandoc_installed()
    return {
        "status": "healthy" if pandoc_installed else "unhealthy",
        "pandoc_installed": pandoc_installed
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
