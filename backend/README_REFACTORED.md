# Markdown to DOCX Converter - Backend API

A modular FastAPI application that converts Markdown files to DOCX format with automatic LaTeX formula conversion.

## Features

- ✅ Convert Markdown text to DOCX via API
- ✅ Upload Markdown files for conversion
- ✅ **Automatic LaTeX formula conversion**:
  - Block formulas: `[formula]` → `$$formula$$`
  - Inline formulas: `( formula = ... )` → `$formula$`
  - Preserves LaTeX bracket commands: `\left[` and `\right]`
- ✅ Modular architecture for easy maintenance
- ✅ CORS enabled for frontend integration

## Project Structure

```
backend/
├── main.py                          # Application entry point
├── web/                             # Web layer
│   ├── routes/                      # API routes
│   │   ├── __init__.py
│   │   └── conversion.py            # Conversion endpoints
│   └── api/                         # (Reserved for future use)
├── utils/                           # Utilities
│   ├── __init__.py
│   ├── config.py                    # Configuration & constants
│   ├── pandoc.py                    # Pandoc conversion functions
│   └── markdown_processor.py        # Markdown preprocessing & LaTeX fixing
├── uploads/                         # File storage
│   ├── md/                          # Uploaded/processed markdown files
│   └── docx/                        # Generated DOCX files
├── requirements.txt                 # Python dependencies
├── test_markdown_processor.py       # Unit tests for markdown processor
└── test_comprehensive.py            # Integration tests
```

## LaTeX Formula Conversion

The application automatically converts LaTeX formulas using an intelligent **spacing rule**:

### The Spacing Rule ⭐

**Inline math**: Content with spaces around it → Convert to `$...$`

| Input | Spaces? | Output |
|-------|---------|--------|
| `\( f(t) \)` | ✅ Yes | `$f(t)$` |
| `( T )` | ✅ Yes | `$T$` |
| `( x )` | ✅ Yes | `$x$` |
| `cos(x)` | ❌ No | `cos(x)` (unchanged) |

**Block math**: Always converted regardless of spacing

| Input | Output |
|-------|--------|
| `\[formula\]` | `$$formula$$` |
| `[formula]` | `$$formula$$` |

### How It Works

The converter uses a simple but powerful rule: **spaces indicate mathematical notation!**

- `( f(t) )` with spaces → variable → `$f(t)$`
- `(x)` without spaces → function argument → stays as `(x)`

This works because:
- Mathematical variables are written with spaces: `( T )`, `( x )`
- Function calls are compact: `cos(x)`, `sin(theta)`

### Supported Notations

The converter supports both standard LaTeX and legacy bracket notation:

| Type | LaTeX Style | Legacy Style | Output |
|------|-------------|--------------|--------|
| **Inline** | `\( var \)` | `( var = ... )` | `$var$` |
| **Block** | `\[formula\]` | `[formula]` | `$$formula$$` |

### Block Formulas

**LaTeX notation:**
```markdown
\[
a_0 = \frac{1}{T} \int_{T} f(t), dt
\]
```

**Legacy notation:**
```markdown
[
a_0 = \frac{1}{T} \int_{T} f(t), dt
]
```

**Both convert to:**
```markdown
$$
a_0 = \frac{1}{T} \int_{T} f(t), dt
$$
```

### Inline Formulas

**LaTeX notation (with spaces):**
```markdown
For a periodic function \( f(t) \) with period \( T \):
```

**Converts to:**
```markdown
For a periodic function $f(t)$ with period $T$:
```

**Function calls (no spaces) stay unchanged:**
```markdown
The function cos(x) and sin(theta)...
→ The function cos(x) and sin(theta)...  (no change!)
```

### Preserving LaTeX Brackets

The processor intelligently preserves `\left[` and `\right]` commands:

**Input:**
```markdown
\[
f(t) = \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]
```

**Output:**
```markdown
$$
f(t) = \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
$$
```

Notice:
- `\[...\]` → `$$...$$` ✅
- `\left[` and `\right]` preserved ✅
- `\cos(n\omega_0 t)` with no spaces stays intact ✅

## API Endpoints

### `POST /convert/text`
Convert markdown text to DOCX.

**Request:**
```json
{
  "markdown": "# Your markdown content",
  "filename": "optional-filename"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversion successful",
  "download_url": "/download/filename.docx",
  "filename": "filename.docx"
}
```

### `POST /convert/upload`
Upload a markdown file and convert to DOCX.

**Request:** Form data with file upload

**Response:**
```json
{
  "success": true,
  "message": "Conversion successful",
  "download_url": "/download/filename.docx",
  "filename": "filename.docx"
}
```

### `GET /download/{filename}`
Download a converted DOCX file.

### `DELETE /cleanup/{filename}`
Delete converted files (both .md and .docx).

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "pandoc_installed": true
}
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Pandoc (required for conversion):
```bash
# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc

# Or download from: https://pandoc.org/installing.html
```

## Running the Server

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## Testing

Run unit tests:
```bash
cd backend
PYTHONPATH=/home/kheyal/dev/mdtodocxbe/backend python3 test_markdown_processor.py
```

Run comprehensive tests:
```bash
cd backend
python3 test_comprehensive.py
```

## Module Documentation

### `utils/markdown_processor.py`
- `fix_latex_formulas(markdown_content)` - Converts LaTeX formulas to proper Markdown format
- `preprocess_markdown(markdown_content)` - Main preprocessing function

### `utils/pandoc.py`
- `check_pandoc_installed()` - Verify Pandoc installation
- `convert_md_to_docx(md_path, docx_path)` - Convert MD to DOCX using Pandoc

### `utils/config.py`
- Constants for directory paths and CORS settings

### `web/routes/conversion.py`
- All conversion-related API endpoints

## Version History

### v2.0.0 (Current)
- ✅ Modular architecture (web/routes, utils)
- ✅ Automatic LaTeX formula conversion
- ✅ **Dual notation support**: Legacy `[...]`/`(...)` AND LaTeX `\[...\]`/`\(...\)`
- ✅ Inline and block formula support
- ✅ Preserves LaTeX bracket commands (`\left[`, `\right]`)

### v1.0.0
- Initial implementation with basic conversion
