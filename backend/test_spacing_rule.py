"""
Test spacing rule for inline formulas
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

# Test 1: LaTeX inline with spaces
test1 = r"""For a periodic function \( f(t) \) with period \( T \):"""

print("=" * 80)
print("TEST 1: LaTeX inline \\( var \\) with spaces")
print("=" * 80)
print("INPUT:", test1)
result1 = preprocess_markdown(test1)
print("OUTPUT:", result1)
print("VERIFY: $f(t)$ present:", "$f(t)$" in result1)
print("VERIFY: $T$ present:", "$T$" in result1)
print()

# Test 2: Normal parentheses WITHOUT spaces (should NOT convert)
test2 = r"""The function cos(x) and sin(x) are trigonometric functions."""

print("=" * 80)
print("TEST 2: Normal parentheses (x) without spaces - should NOT convert")
print("=" * 80)
print("INPUT:", test2)
result2 = preprocess_markdown(test2)
print("OUTPUT:", result2)
print("VERIFY: cos(x) unchanged:", "cos(x)" in result2)
print("VERIFY: sin(x) unchanged:", "sin(x)" in result2)
print("VERIFY: No $ added:", result2.count('$') == 0)
print()

# Test 3: Mixed - some with spaces, some without
test3 = r"""Calculate cos(theta) where \( \theta \) is the angle."""

print("=" * 80)
print("TEST 3: Mixed - cos(theta) without spaces, \\( \\theta \\) with spaces")
print("=" * 80)
print("INPUT:", test3)
result3 = preprocess_markdown(test3)
print("OUTPUT:", result3)
print("VERIFY: cos(theta) unchanged:", "cos(theta)" in result3)
print("VERIFY: \\theta converted:", "$\\theta$" in result3)
print()

# Test 4: Legacy inline with spaces
test4 = r"""Using Euler's identity ( e^{j\theta} = \cos\theta + j\sin\theta ):"""

print("=" * 80)
print("TEST 4: Legacy inline ( formula ) with spaces")
print("=" * 80)
print("INPUT:", test4)
result4 = preprocess_markdown(test4)
print("OUTPUT:", result4)
print("VERIFY: Converted to inline $:", "$e^{j\\theta}" in result4)
print()

# Test 5: Block formula
test5 = r"""\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]"""

print("=" * 80)
print("TEST 5: Block formula \\[...\\]")
print("=" * 80)
print("INPUT:")
print(test5)
result5 = preprocess_markdown(test5)
print("\nOUTPUT:")
print(result5)
print("\nVERIFY: Block $$ present:", "$$" in result5)
print("VERIFY: \\left[ preserved:", "\\left[" in result5)
print("VERIFY: \\right] preserved:", "\\right]" in result5)
print("VERIFY: cos(n\\omega_0 t) unchanged:", "cos(n\\omega_0 t)" in result5 or "\\cos(n\\omega_0 t)" in result5)
print()

# Test 6: Real-world complete example
test6 = r"""For a periodic function \( f(t) \) with period \( T \):
\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]

where \( \omega_0 = \frac{2\pi}{T} \) is the fundamental frequency.

The coefficients are:
\[
a_0 = \frac{1}{T} \int_{T} f(t)\, dt
\]"""

print("=" * 80)
print("TEST 6: Complete real-world example")
print("=" * 80)
print("INPUT:")
print(test6)
result6 = preprocess_markdown(test6)
print("\nOUTPUT:")
print(result6)
print("\nVERIFICATION:")
print("  ✓ $f(t)$ converted:", "$f(t)$" in result6)
print("  ✓ $T$ converted:", "$T$" in result6)
print("  ✓ $\\omega_0 = ...$  converted:", "$\\omega_0 = " in result6)
print("  ✓ Block formulas ($$):", result6.count("$$") >= 4)
print("  ✓ \\left[ preserved:", "\\left[" in result6)
print("  ✓ Function calls like cos(x) intact:", "cos(n" in result6 or "\\cos(n" in result6)
print()

print("=" * 80)
print("✅ ALL SPACING RULE TESTS COMPLETED")
print("=" * 80)
