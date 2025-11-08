#!/usr/bin/env python3
"""
Comprehensive test for legacy parentheses notation
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

print("=" * 80)
print("COMPREHENSIVE TEST: Legacy ( var ) notation")
print("=" * 80)

# Test 1: Simple variables (should convert)
test1 = """For a function ( f(t) ) with period ( T ):"""
result1 = preprocess_markdown(test1)
print("\nTest 1: Simple variables")
print("INPUT: ", test1)
print("OUTPUT:", result1)
print("PASS:", "$f(t)$" in result1 and "$T$" in result1)

# Test 2: Longer text in parentheses (should NOT convert)
test2 = """This is a note ( written in parentheses ) for clarity."""
result2 = preprocess_markdown(test2)
print("\nTest 2: Longer text (should NOT convert)")
print("INPUT: ", test2)
print("OUTPUT:", result2)
print("PASS:", "written in parentheses" in result2 and result2.count('$') == 0)

# Test 3: Mixed - some short, some long
test3 = """The variable ( x ) is used in the equation ( this is a longer note about x )."""
result3 = preprocess_markdown(test3)
print("\nTest 3: Mixed short and long")
print("INPUT: ", test3)
print("OUTPUT:", result3)
print("PASS:", "$x$" in result3 and "this is a longer note" in result3)

# Test 4: Edge case - exactly 6 characters
test4 = """Value ( abc123 ) versus ( abcdef ) in text."""
result4 = preprocess_markdown(test4)
print("\nTest 4: Length edge cases (6 chars)")
print("INPUT: ", test4)
print("OUTPUT:", result4)
print("PASS:", "$abc123$" in result4 and "$abcdef$" in result4)

# Test 5: With equations (should always convert)
test5 = """Using ( e^{j\\theta} = \\cos\\theta + j\\sin\\theta ) we get..."""
result5 = preprocess_markdown(test5)
print("\nTest 5: Equation (should always convert)")
print("INPUT: ", test5)
print("OUTPUT:", result5)
print("PASS:", "$e^{j" in result5)

# Test 6: Without spaces (should NOT convert)
test6 = """The function sin(x) and cos(theta) are used."""
result6 = preprocess_markdown(test6)
print("\nTest 6: No spaces (should NOT convert)")
print("INPUT: ", test6)
print("OUTPUT:", result6)
print("PASS:", "sin(x)" in result6 and "cos(theta)" in result6 and result6.count('$') == 0)

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED")
print("=" * 80)
