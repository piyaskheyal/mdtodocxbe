"""
Comprehensive test with user's examples
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

# User's original example 1
test1 = """```
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

print("=" * 80)
print("TEST 1: Original example with block formulas")
print("=" * 80)
print("INPUT:")
print(test1)
print("\nOUTPUT:")
result1 = preprocess_markdown(test1)
print(result1)
print()

# User's second example with inline and block
test2 = """Using Euler's identity ( e^{j\\theta} = \\cos\\theta + j\\sin\\theta ):
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

print("=" * 80)
print("TEST 2: Mixed inline and block formulas")
print("=" * 80)
print("INPUT:")
print(test2)
print("\nOUTPUT:")
result2 = preprocess_markdown(test2)
print(result2)
print()

# User's third example with \left[ and \right]
test3 = """For a periodic function ( f(t) ) with period ( T ):
[
f(t) = a_0 + \\sum_{n=1}^{\\infty} \\left[ a_n \\cos(n\\omega_0 t) + b_n \\sin(n\\omega_0 t) \\right]
]"""

print("=" * 80)
print("TEST 3: Block formula with \\left[ and \\right] (should be preserved)")
print("=" * 80)
print("INPUT:")
print(test3)
print("\nOUTPUT:")
result3 = preprocess_markdown(test3)
print(result3)
print()

# Verification
print("=" * 80)
print("VERIFICATION")
print("=" * 80)
print("Test 1: Block formulas converted to $$...$$:", "$$" in result1 and "[" not in result1.replace("```", ""))
print("Test 2: Inline formula converted:", "$e^{j\\theta}" in result2)
print("Test 2: Block formulas converted:", result2.count("$$") >= 6)
print("Test 3: \\left[ preserved:", "\\left[" in result3)
print("Test 3: \\right] preserved:", "\\right]" in result3)
print("Test 3: Block formula converted:", "$$" in result3)
