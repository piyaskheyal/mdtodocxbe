# Prompt for Frontend Developer (React)

## Project Overview

I need you to create a **React frontend** for a Markdown to DOCX converter web application. The backend API is already built and running on `http://localhost:8000`.

---

## Project Goal

Build a clean, modern, user-friendly React application where users can:
1. **Paste markdown text** into a textarea and convert it to DOCX
2. **Upload a `.md` file** and convert it to DOCX
3. **Download** the converted DOCX file

---

## Backend API Details

The FastAPI backend is ready and provides these endpoints:

### 1. Convert Text to DOCX
- **Endpoint**: `POST http://localhost:8000/convert/text`
- **Request Body** (JSON):
  ```json
  {
    "markdown": "# Hello World\n\nThis is **markdown**",
    "filename": "my-document"  // optional
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Conversion successful",
    "download_url": "/download/my-document_a1b2c3d4.docx",
    "filename": "my-document_a1b2c3d4.docx"
  }
  ```

### 2. Upload File and Convert
- **Endpoint**: `POST http://localhost:8000/convert/upload`
- **Request**: FormData with file field
- **Response**: Same as above

### 3. Download File
- **Endpoint**: `GET http://localhost:8000/download/{filename}`
- **Response**: DOCX file download

### 4. Health Check
- **Endpoint**: `GET http://localhost:8000/health`
- **Response**:
  ```json
  {
    "status": "healthy",
    "pandoc_installed": true
  }
  ```

**Note**: CORS is already configured on the backend for localhost ports 3000, 5173, and 8080.

---

## Frontend Requirements

### Tech Stack
- **React** (latest version with hooks)
- **Vite** (for fast development)
- **CSS** (use your choice: plain CSS, Tailwind CSS, or Material-UI)
- **Fetch API** or **Axios** for HTTP requests

### Features Required

#### 1. **Two-Tab/Two-Section Interface**
- **Tab/Section 1**: Paste Markdown Text
  - Large textarea for pasting markdown
  - Optional input field for custom filename
  - "Convert to DOCX" button
  - Preview area showing the markdown (optional but nice to have)

- **Tab/Section 2**: Upload Markdown File
  - File input accepting only `.md` files
  - Drag-and-drop support (optional but recommended)
  - "Upload and Convert" button

#### 2. **Conversion Flow**
- Show loading state during conversion
- Display success message with download button/link
- Handle errors gracefully (show error messages)

#### 3. **Download Functionality**
- Automatic download trigger when conversion succeeds
- Or display a "Download DOCX" button

#### 4. **UI/UX Features**
- Clean, modern design
- Responsive (works on mobile and desktop)
- Loading spinners/indicators
- Success/error notifications or toast messages
- Clear button to reset the form
- Sample markdown text in placeholder or example section

#### 5. **Error Handling**
- Empty input validation
- Network error handling
- Backend error messages displayed to user
- File type validation (only .md files)

### Nice-to-Have Features (Optional)
- Markdown live preview (show formatted markdown before conversion)
- Dark mode toggle
- History of converted files (stored in localStorage)
- Copy markdown from clipboard button
- Sample markdown templates to try
- File size validation
- Progress bar during upload

---

## Project Structure

Use Vite for project setup. Suggested structure:

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── TextConverter.jsx       # Tab 1: Paste text
│   │   ├── FileUploader.jsx        # Tab 2: Upload file
│   │   ├── DownloadButton.jsx      # Download component
│   │   ├── LoadingSpinner.jsx      # Loading state
│   │   └── ErrorMessage.jsx        # Error display
│   ├── services/
│   │   └── api.js                  # API calls to backend
│   ├── App.jsx                     # Main app component
│   ├── App.css                     # Styles
│   └── main.jsx                    # Entry point
├── package.json
├── vite.config.js
└── README.md
```

---

## API Integration Examples

### JavaScript Fetch (Text Conversion)
```javascript
async function convertText(markdown, filename) {
  const response = await fetch('http://localhost:8000/convert/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ markdown, filename })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Conversion failed');
  }
  
  return await response.json();
}
```

### JavaScript Fetch (File Upload)
```javascript
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/convert/upload', {
    method: 'POST',
    body: formData
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }
  
  return await response.json();
}
```

### Download File
```javascript
function downloadFile(downloadUrl, filename) {
  const link = document.createElement('a');
  link.href = `http://localhost:8000${downloadUrl}`;
  link.download = filename;
  link.click();
}
```

---

## Setup Instructions to Include

Create a `README.md` in the frontend directory with:

1. **Installation**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

4. **Prerequisites**:
   - Node.js 16+ installed
   - Backend server running on `http://localhost:8000`

---

## Design Guidelines

### Color Scheme (Suggestion)
- Primary: Blue (#007bff)
- Success: Green (#28a745)
- Error: Red (#dc3545)
- Background: Light gray or white
- Text: Dark gray (#333)

### Layout
- Center-aligned, max-width container (800-1000px)
- Clean spacing and padding
- Clear visual hierarchy
- Responsive grid/flexbox layout

### Accessibility
- Proper labels for inputs
- Keyboard navigation support
- ARIA attributes where needed
- Good color contrast

---

## Example Markdown to Use in Placeholder

```markdown
# Hello World

This is a **bold** text and this is *italic*.

## Features

- Tables
- Lists
- Code blocks
- Math formulas

## Sample Table

| Name | Age | City |
|------|-----|------|
| John | 30  | NYC  |
| Jane | 25  | LA   |

## Code Example

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`

## Math Formula

The quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$
```

---

## Deliverables

1. **Complete React app** with Vite setup
2. **package.json** with all dependencies
3. **README.md** with setup and run instructions
4. **Clean, commented code**
5. **Working conversion for both methods** (paste and upload)
6. **Error handling** for all edge cases
7. **Responsive design** that works on mobile

---

## Testing Checklist

Before submitting, ensure:
- ✅ Text paste conversion works
- ✅ File upload conversion works
- ✅ Download button/link works
- ✅ Error messages display correctly
- ✅ Loading states show during API calls
- ✅ Empty input validation works
- ✅ Only .md files can be uploaded
- ✅ Responsive on mobile and desktop
- ✅ Backend server connection configured correctly

---

## Additional Notes

- Backend server must be running before testing frontend
- CORS is already configured, no proxy needed
- Use environment variables for API base URL (e.g., `VITE_API_URL`)
- The backend supports markdown with tables, formulas (LaTeX), code blocks, and more

---

## Questions to Clarify (if needed)

1. Do you want me to use a specific CSS framework? (Tailwind, Material-UI, Bootstrap, or plain CSS?)
2. Should I add markdown preview functionality?
3. Do you want tabs or a single-page layout with both sections visible?
4. Any specific color scheme or branding?

---

## Start Command

To get started:
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios  # if using axios instead of fetch
npm run dev
```

Then build the components as specified above!

---

**Goal**: Create a beautiful, functional React frontend that integrates seamlessly with the existing FastAPI backend for converting Markdown to DOCX files.
