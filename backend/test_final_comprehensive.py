#!/usr/bin/env python3
"""
Final comprehensive test including tables
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

test = r"""# Partial Differential Equations

For a second-order PDE of the form:
\[
A\frac{\partial^2 u}{\partial x^2} + B\frac{\partial^2 u}{\partial x \partial y} + C\frac{\partial^2 u}{\partial y^2} + \ldots = 0
\]

Classification based on the discriminant ( B^2 - 4AC ):

| Type       | Condition         | Example            |
| ---------- | ----------------- | ------------------ |
| Elliptic   | ( B^2 - 4AC < 0 ) | Laplace's equation |
| Parabolic  | ( B^2 - 4AC = 0 ) | Heat equation      |
| Hyperbolic | ( B^2 - 4AC > 0 ) | Wave equation      |

For a function \( u(x,y) \) where ( x ) and ( y ) are independent variables.

Note: The determinant formula det(A) is used, but ( det(A) ) with spaces converts."""

print("╔" + "═" * 78 + "╗")
print("║" + " " * 10 + "COMPREHENSIVE TEST: Tables + All Notations" + " " * 25 + "║")
print("╚" + "═" * 78 + "╝")
print()

print("📥 INPUT:")
print("─" * 80)
print(test)
print()

result = preprocess_markdown(test)

print("📤 OUTPUT:")
print("─" * 80)
print(result)
print()

print("✅ VERIFICATION:")
print("─" * 80)
checks = [
    ("Block formula \\[...\\] converted", "$$" in result),
    ("( B^2 - 4AC ) in text converted", result.count("$B^2 - 4AC$") >= 1),
    ("( B^2 - 4AC < 0 ) in table converted", "$B^2 - 4AC < 0$" in result),
    ("( B^2 - 4AC = 0 ) in table converted", "$B^2 - 4AC = 0$" in result),
    ("( B^2 - 4AC > 0 ) in table converted", "$B^2 - 4AC > 0$" in result),
    ("LaTeX inline \\( u(x,y) \\) converted", "$u(x,y)$" in result),
    ("Simple variables ( x ) and ( y ) converted", "$x$" in result and "$y$" in result),
    ("Function det(A) without spaces preserved", "det(A)" in result),
    ("Variable ( det(A) ) with spaces converted", "$det(A)$" in result),
    ("Table structure preserved", "|" in result and "---" in result),
]

all_passed = True
for check, passed in checks:
    status = "✓" if passed else "✗"
    print(f"  {status} {check}")
    if not passed:
        all_passed = False

print()
if all_passed:
    print("🎉 PERFECT! All edge cases handled correctly!")
else:
    print("❌ Some checks failed")
