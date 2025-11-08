"""
Markdown processing utilities for converting and fixing markdown content
"""
import re


def fix_latex_formulas(markdown_content: str) -> str:
    r"""
    Convert LaTeX formulas from various notations to proper markdown format.
    
    Rules:
    - Block formulas: \[...\] or [...] -> $$...$$
    - Inline formulas with spaces: \( var \) or ( var ) -> $var$
    - Inline without spaces: (var) -> keep as is (normal parentheses)
    
    Args:
        markdown_content: The markdown content with LaTeX formulas
        
    Returns:
        Corrected markdown content with proper LaTeX delimiters
    """
    if not markdown_content:
        return markdown_content
    
    # Handle LaTeX-style block delimiters: \[ ... \]
    # This is the standard LaTeX notation that ChatGPT uses
    # Use raw string and re.DOTALL to match across newlines
    latex_block_pattern = r'\\\[\s*((?:[^\\]|\\(?!\]))+?)\s*\\\]'
    
    def replace_latex_block(match):
        formula = match.group(1).strip()
        return f"\n$$\n{formula}\n$$\n"
    
    markdown_content = re.sub(latex_block_pattern, replace_latex_block, markdown_content, flags=re.DOTALL)
    
    # Handle LaTeX-style inline delimiters: \( ... \)
    # This is the standard LaTeX notation for inline math
    # Only convert if there are spaces around the content (indicates it's a variable/formula)
    latex_inline_pattern = r'\\\(\s+(.+?)\s+\\\)'
    
    def replace_latex_inline(match):
        formula = match.group(1).strip()
        return f"${formula}$"
    
    markdown_content = re.sub(latex_inline_pattern, replace_latex_inline, markdown_content)
    
    # Pattern to match formulas in square brackets (legacy notation)
    # This matches formulas that are on their own lines (block formulas)
    # Example: [\na_0 = \frac{1}{T} \int_{T} f(t), dt\n]
    # We need to be careful not to replace \left[ and \right[ inside the formula
    block_formula_pattern = r'^\s*\[\s*\n((?:[^\[\]]|\\left\[|\\right\[|\\left\]|\\right\]|\n)+?)\n\s*\]\s*$'
    
    # Replace block formulas (multiline formulas in brackets)
    def replace_block_formula(match):
        formula = match.group(1).strip()
        return f"\n$$\n{formula}\n$$\n"
    
    # Process block formulas
    markdown_content = re.sub(
        block_formula_pattern,
        replace_block_formula,
        markdown_content,
        flags=re.MULTILINE
    )
    
    # Pattern to match single-line formulas in brackets
    # Example: [ a_0 = \frac{1}{T} \int_{T} f(t), dt ]
    # Also allow \left[ and \right] inside
    single_line_block_pattern = r'^\s*\[\s*([^\[\]\n]*(?:\\left\[|\\right\[|\\left\]|\\right\]|[^\[\]\n])*?)\s*\]\s*$'
    
    def replace_single_line_formula(match):
        formula = match.group(1).strip()
        # Check if it contains LaTeX commands (likely a formula)
        if '\\' in formula or '_' in formula or '^' in formula:
            return f"\n$$\n{formula}\n$$\n"
        # Otherwise, keep it as is (might be a regular bracket)
        return match.group(0)
    
    # Process single-line block formulas
    markdown_content = re.sub(
        single_line_block_pattern,
        replace_single_line_formula,
        markdown_content,
        flags=re.MULTILINE
    )
    
    # Pattern to match inline formulas in parentheses with spaces: ( formula )
    # Only convert if there are spaces after ( and before )
    # This distinguishes math variables from normal parentheses like (x) in function calls
    inline_paren_formula_pattern = r'\(\s+(.+?)\s+\)'
    
    def replace_paren_inline_formula(match):
        formula = match.group(1).strip()
        
        # Convert if it looks like a formula or variable:
        # 1. Contains LaTeX commands (backslash)
        # 2. Contains subscripts/superscripts with braces
        # 3. Has mathematical operators: =, <, >, ≤, ≥, ≠
        # 4. Contains both ^ (superscript) and math symbols
        # 5. Is short (≤6 chars) - likely a variable like T, x, f(t)
        has_latex = '\\' in formula
        has_subscript_superscript = ('^' in formula and '{' in formula) or ('_' in formula and '{' in formula)
        has_math_operator = any(op in formula for op in ['=', '<', '>', '≤', '≥', '≠'])
        has_superscript_simple = '^' in formula  # Like B^2
        is_short = len(formula) <= 6
        
        if (has_latex or 
            has_subscript_superscript or 
            has_math_operator or
            (has_superscript_simple and any(c in formula for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/')) or
            is_short):
            return f"${formula}$"
        # Otherwise, keep it as is
        return match.group(0)
    
    # Pattern to match inline formulas in brackets within text
    # Example: The formula [x = y] is simple
    # Only convert if it contains LaTeX commands
    # But NOT if it's preceded by \left or \right (those are LaTeX bracket commands)
    inline_formula_pattern = r'(?<!\\left)(?<!\\right)\[([^\[\]\n]+?)\](?!\$)'
    
    def replace_inline_formula(match):
        formula = match.group(1).strip()
        # Only convert if it looks like a formula (contains LaTeX commands)
        if ('\\' in formula or ('_' in formula and '{' in formula) or 
            ('^' in formula and '{' in formula)):
            return f"${formula}$"
        # Otherwise, keep it as is (might be a regular bracket)
        return match.group(0)
    
    # Process inline formulas (only within text, not on their own lines)
    lines = markdown_content.split('\n')
    processed_lines = []
    
    for line in lines:
        # Skip if line is already a block formula or empty or contains \left[ or \right]
        if (line.strip().startswith('$$') or not line.strip() or 
            '\\left[' in line or '\\right]' in line):
            processed_lines.append(line)
            continue
        
        # Process inline formulas in parentheses first
        processed_line = re.sub(inline_paren_formula_pattern, replace_paren_inline_formula, line)
        # Then process inline formulas in brackets
        processed_line = re.sub(inline_formula_pattern, replace_inline_formula, processed_line)
        processed_lines.append(processed_line)
    
    # Clean up multiple consecutive blank lines
    result = '\n'.join(processed_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result


def preprocess_markdown(markdown_content: str) -> str:
    """
    Preprocess markdown content before conversion to DOCX.
    
    This function applies various transformations to ensure proper rendering:
    - Fixes LaTeX formula notation
    - Can be extended with other preprocessing steps
    
    Args:
        markdown_content: The original markdown content
        
    Returns:
        Preprocessed markdown content
    """
    # Fix LaTeX formulas
    markdown_content = fix_latex_formulas(markdown_content)
    
    # Additional preprocessing can be added here
    # For example:
    # - Fixing image paths
    # - Normalizing line endings
    # - Cleaning up special characters
    
    return markdown_content
