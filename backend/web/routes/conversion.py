"""
Conversion API routes for markdown to DOCX conversion
"""
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from utils import (
    check_pandoc_installed,
    convert_md_to_docx,
    preprocess_markdown,
    MD_DIR,
    DOCX_DIR
)

router = APIRouter()


class MarkdownTextRequest(BaseModel):
    markdown: str
    filename: Optional[str] = None


@router.post("/convert/text")
async def convert_text_to_docx(request: MarkdownTextRequest):
    """
    Convert markdown text to DOCX
    
    Request body:
    - markdown: The markdown text content
    - filename: Optional custom filename (without extension)
    
    Returns:
    - download_url: URL to download the converted DOCX file
    - filename: Name of the converted file
    """
    if not check_pandoc_installed():
        raise HTTPException(
            status_code=500,
            detail="Pandoc is not installed on the server. Please contact the administrator."
        )
    
    if not request.markdown or not request.markdown.strip():
        raise HTTPException(status_code=400, detail="Markdown content is required")
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())
    base_filename = request.filename or f"converted_{unique_id[:8]}"
    
    # Remove any file extensions if provided
    base_filename = base_filename.replace(".md", "").replace(".docx", "")
    
    md_filename = f"{base_filename}_{unique_id[:8]}.md"
    docx_filename = f"{base_filename}_{unique_id[:8]}.docx"
    
    md_file_path = MD_DIR / md_filename
    docx_file_path = DOCX_DIR / docx_filename
    
    try:
        # Preprocess markdown content (fix LaTeX formulas, etc.)
        processed_markdown = preprocess_markdown(request.markdown)
        
        # Write processed markdown content to file
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(processed_markdown)
        
        # Convert to DOCX
        success = convert_md_to_docx(md_file_path, docx_file_path)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to convert markdown to DOCX. Please check your markdown syntax."
            )
        
        # Return download URL
        return {
            "success": True,
            "message": "Conversion successful",
            "download_url": f"/download/{docx_filename}",
            "filename": docx_filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during conversion: {str(e)}"
        )


@router.post("/convert/upload")
async def convert_upload_to_docx(file: UploadFile = File(...)):
    """
    Upload a markdown file and convert to DOCX
    
    Form data:
    - file: The markdown file to upload
    
    Returns:
    - download_url: URL to download the converted DOCX file
    - filename: Name of the converted file
    """
    if not check_pandoc_installed():
        raise HTTPException(
            status_code=500,
            detail="Pandoc is not installed on the server. Please contact the administrator."
        )
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename.endswith(".md"):
        raise HTTPException(
            status_code=400,
            detail="Only markdown files (.md) are supported"
        )
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())
    base_filename = file.filename.replace(".md", "")
    
    md_filename = f"{base_filename}_{unique_id[:8]}.md"
    docx_filename = f"{base_filename}_{unique_id[:8]}.docx"
    
    md_file_path = MD_DIR / md_filename
    docx_file_path = DOCX_DIR / docx_filename
    
    try:
        # Read uploaded file content
        content = await file.read()
        markdown_content = content.decode('utf-8')
        
        # Preprocess markdown content (fix LaTeX formulas, etc.)
        processed_markdown = preprocess_markdown(markdown_content)
        
        # Save processed file
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(processed_markdown)
        
        # Convert to DOCX
        success = convert_md_to_docx(md_file_path, docx_file_path)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to convert markdown to DOCX. Please check your markdown syntax."
            )
        
        # Return download URL
        return {
            "success": True,
            "message": "Conversion successful",
            "download_url": f"/download/{docx_filename}",
            "filename": docx_filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during conversion: {str(e)}"
        )


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a converted DOCX file
    
    Path parameter:
    - filename: Name of the file to download
    """
    file_path = DOCX_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Invalid file")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.delete("/cleanup/{filename}")
async def cleanup_files(filename: str):
    """
    Delete converted files (both .md and .docx)
    
    Path parameter:
    - filename: Base filename (without extension)
    """
    deleted_files = []
    
    # Try to delete both md and docx versions
    for directory, extension in [(MD_DIR, ".md"), (DOCX_DIR, ".docx")]:
        file_path = directory / f"{filename}{extension}"
        if file_path.exists():
            try:
                os.remove(file_path)
                deleted_files.append(str(file_path))
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    
    return {
        "success": True,
        "deleted_files": deleted_files
    }
