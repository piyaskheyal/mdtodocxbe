#!/usr/bin/env python3
"""
Test script for the Markdown to DOCX Converter API
This demonstrates how to use both endpoints from Python
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_text_conversion():
    """Test converting markdown text to DOCX"""
    print("📝 Testing text conversion...")
    
    markdown_text = """# Sample Document

This is a **bold** and *italic* text example.

## Features

- Tables
- Lists
- Code blocks

## Table Example

| Name | Age | City |
|------|-----|------|
| Alice | 30  | NYC  |
| Bob   | 25  | LA   |

## Math Formula

The quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$

## Code Block

```python
def greet(name):
    return f"Hello, {name}!"
```
"""
    
    response = requests.post(
        f"{BASE_URL}/convert/text",
        json={
            "markdown": markdown_text,
            "filename": "sample-document"
        }
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        # Download the file
        download_url = result["download_url"]
        filename = result["filename"]
        
        print(f"\n⬇️  Downloading {filename}...")
        file_response = requests.get(f"{BASE_URL}{download_url}")
        
        with open(f"/tmp/{filename}", "wb") as f:
            f.write(file_response.content)
        
        print(f"✅ File saved to /tmp/{filename}\n")
    else:
        print("❌ Conversion failed\n")

def test_file_upload():
    """Test uploading a markdown file"""
    print("📤 Testing file upload...")
    
    # Create a test markdown file
    test_md = """# Upload Test

This is a test file uploaded to the API.

## List

1. First item
2. Second item
3. Third item
"""
    
    with open("/tmp/test-upload.md", "w") as f:
        f.write(test_md)
    
    # Upload the file
    with open("/tmp/test-upload.md", "rb") as f:
        files = {"file": ("test-upload.md", f, "text/markdown")}
        response = requests.post(f"{BASE_URL}/convert/upload", files=files)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        # Download the file
        download_url = result["download_url"]
        filename = result["filename"]
        
        print(f"\n⬇️  Downloading {filename}...")
        file_response = requests.get(f"{BASE_URL}{download_url}")
        
        with open(f"/tmp/{filename}", "wb") as f:
            f.write(file_response.content)
        
        print(f"✅ File saved to /tmp/{filename}\n")
    else:
        print("❌ Upload/conversion failed\n")

def test_error_handling():
    """Test error handling"""
    print("🚨 Testing error handling...")
    
    # Test with empty markdown
    response = requests.post(
        f"{BASE_URL}/convert/text",
        json={"markdown": ""}
    )
    print(f"Empty markdown - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test with wrong file type
    with open("/tmp/test.txt", "w") as f:
        f.write("This is not a markdown file")
    
    with open("/tmp/test.txt", "rb") as f:
        files = {"file": ("test.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/convert/upload", files=files)
    
    print(f"Wrong file type - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Markdown to DOCX Converter API - Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_text_conversion()
        test_file_upload()
        test_error_handling()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
