"""
Pandoc conversion utilities
"""
import subprocess
from pathlib import Path


def check_pandoc_installed() -> bool:
    """
    Check if pandoc is installed on the system
    
    Returns:
        True if pandoc is available, False otherwise
    """
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def convert_md_to_docx(md_file_path: Path, docx_file_path: Path) -> bool:
    """
    Convert markdown file to docx using system pandoc
    
    Args:
        md_file_path: Path to the input markdown file
        docx_file_path: Path to the output DOCX file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        result = subprocess.run(
            ["pandoc", str(md_file_path), "-o", str(docx_file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Pandoc error: {result.stderr}")
            return False
        
        return docx_file_path.exists()
    
    except subprocess.TimeoutExpired:
        print("Pandoc conversion timed out")
        return False
    except Exception as e:
        print(f"Conversion error: {str(e)}")
        return False
