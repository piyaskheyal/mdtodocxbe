#!/bin/bash

# Quick verification script for the refactored backend

echo "=========================================="
echo "Backend Refactoring Verification"
echo "=========================================="
echo ""

cd /home/kheyal/dev/mdtodocxbe/backend

# Check if all required files exist
echo "1. Checking file structure..."
files=(
    "main.py"
    "web/routes/__init__.py"
    "web/routes/conversion.py"
    "utils/__init__.py"
    "utils/config.py"
    "utils/pandoc.py"
    "utils/markdown_processor.py"
)

all_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (MISSING)"
        all_exist=false
    fi
done

if [ "$all_exist" = true ]; then
    echo "   All files present!"
else
    echo "   Some files are missing!"
    exit 1
fi

echo ""

# Check Python imports
echo "2. Checking Python imports..."
python3 -c "
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')
try:
    from utils import check_pandoc_installed, convert_md_to_docx, preprocess_markdown
    from web.routes import conversion_router
    print('   ✓ All imports successful')
except ImportError as e:
    print(f'   ✗ Import error: {e}')
    sys.exit(1)
"

echo ""

# Check Pandoc
echo "3. Checking Pandoc installation..."
python3 -c "
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')
from utils import check_pandoc_installed
if check_pandoc_installed():
    print('   ✓ Pandoc is installed')
else:
    print('   ✗ Pandoc is NOT installed')
    sys.exit(1)
"

echo ""

# Run tests
echo "4. Running LaTeX formula conversion tests..."
PYTHONPATH=/home/kheyal/dev/mdtodocxbe/backend python3 test_comprehensive.py > /tmp/test_output.txt 2>&1

if grep -q "Test 1: Block formulas converted to \$\$...\$\$: True" /tmp/test_output.txt && \
   grep -q "Test 2: Inline formula converted: True" /tmp/test_output.txt && \
   grep -q "Test 3: \\\\left\[ preserved: True" /tmp/test_output.txt; then
    echo "   ✓ All tests passed"
else
    echo "   ✗ Some tests failed"
    cat /tmp/test_output.txt
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ All checks passed!"
echo "=========================================="
echo ""
echo "To start the server:"
echo "  cd /home/kheyal/dev/mdtodocxbe/backend"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
