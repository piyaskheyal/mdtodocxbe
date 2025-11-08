"""
Test script for markdown processing utilities
"""
from utils.markdown_processor import fix_latex_formulas, preprocess_markdown


def test_latex_formula_conversion():
    """Test the LaTeX formula conversion function"""
    
    # Test case 1: Block formulas with square brackets (multiline)
    test_md_1 = """# Test Document

Some text before

[
a_0 = \\frac{1}{T} \\int_{T} f(t), dt
]

Some text after"""

    expected_1 = """# Test Document

Some text before

$$
a_0 = \\frac{1}{T} \\int_{T} f(t), dt
$$

Some text after"""
    
    result_1 = fix_latex_formulas(test_md_1)
    print("Test 1 - Multiline block formula:")
    print("Input:")
    print(test_md_1)
    print("\nExpected:")
    print(expected_1)
    print("\nResult:")
    print(result_1)
    print("\nPassed:", result_1 == expected_1)
    print("-" * 80)
    
    # Test case 2: Multiple block formulas
    test_md_2 = """# Formulas

[
a_0 = \\frac{1}{T} \\int_{T} f(t), dt
]

[
a_n = \\frac{2}{T} \\int_{T} f(t)\\cos(n\\omega_0 t), dt
]

[
b_n = \\frac{2}{T} \\int_{T} f(t)\\sin(n\\omega_0 t), dt
]
"""

    result_2 = fix_latex_formulas(test_md_2)
    print("\nTest 2 - Multiple block formulas:")
    print("Input:")
    print(test_md_2)
    print("\nResult:")
    print(result_2)
    print("\nContains $$:", "$$" in result_2)
    print("Contains [:", "[" not in result_2 or "\\[" in result_2)
    print("-" * 80)
    
    # Test case 3: Single line formula
    test_md_3 = """# Test

[ x = \\frac{y}{z} ]

Some text"""

    result_3 = fix_latex_formulas(test_md_3)
    print("\nTest 3 - Single line formula:")
    print("Input:")
    print(test_md_3)
    print("\nResult:")
    print(result_3)
    print("\nContains $$:", "$$" in result_3)
    print("-" * 80)
    
    # Test case 4: Inline formula (shouldn't be converted unless clear LaTeX)
    test_md_4 = """Text with [some brackets] and [x = \\frac{a}{b}] formula."""
    
    result_4 = fix_latex_formulas(test_md_4)
    print("\nTest 4 - Mixed brackets and inline formula:")
    print("Input:")
    print(test_md_4)
    print("\nResult:")
    print(result_4)
    print("-" * 80)
    
    # Test case 5: The actual user's example
    test_md_5 = """```
[
a_0 = \\frac{1}{T} \\int_{T} f(t), dt
]

[
a_n = \\frac{2}{T} \\int_{T} f(t)\\cos(n\\omega_0 t), dt
]

[
b_n = \\frac{2}{T} \\int_{T} f(t)\\sin(n\\omega_0 t), dt
]
```"""
    
    result_5 = fix_latex_formulas(test_md_5)
    print("\nTest 5 - User's example:")
    print("Input:")
    print(test_md_5)
    print("\nResult:")
    print(result_5)
    print("-" * 80)
    
    # Test case 6: User's second example with inline formulas in parentheses
    test_md_6 = """Using Euler's identity ( e^{j\\theta} = \\cos\\theta + j\\sin\\theta ):
[
f(t) = \\sum_{n=-\\infty}^{\\infty} c_n e^{j n \\omega_0 t}
]
with coefficients
[
c_n = \\frac{1}{T} \\int_{T} f(t) e^{-j n \\omega_0 t} , dt
]

And relation between coefficients:
[
a_n = 2 \\text{Re}(c_n), \\quad b_n = -2 \\text{Im}(c_n)
]"""
    
    result_6 = fix_latex_formulas(test_md_6)
    print("\nTest 6 - Mixed inline (parentheses) and block formulas:")
    print("Input:")
    print(test_md_6)
    print("\nResult:")
    print(result_6)
    print("\nContains inline formula with $:", "$e^{j" in result_6)
    print("Parentheses removed for inline:", "( e^{j" not in result_6)
    print("Block formulas with $$:", result_6.count("$$") >= 6)
    print("-" * 80)
    
    # Test case 7: Block formula containing \left[ and \right] (literal brackets)
    test_md_7 = """For a periodic function ( f(t) ) with period ( T ):
[
f(t) = a_0 + \\sum_{n=1}^{\\infty} \\left[ a_n \\cos(n\\omega_0 t) + b_n \\sin(n\\omega_0 t) \\right]
]"""
    
    result_7 = fix_latex_formulas(test_md_7)
    print("\nTest 7 - Block formula with \\left[ and \\right] inside:")
    print("Input:")
    print(test_md_7)
    print("\nResult:")
    print(result_7)
    print("\nContains $$:", "$$" in result_7)
    print("Preserves \\left[:", "\\left[" in result_7)
    print("Preserves \\right]:", "\\right]" in result_7)
    print("Inline formulas converted:", "$f(t)$" in result_7 and "$T$" in result_7)
    print("-" * 80)


if __name__ == "__main__":
    test_latex_formula_conversion()
