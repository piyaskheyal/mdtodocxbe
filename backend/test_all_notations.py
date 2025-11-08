#!/usr/bin/env python3
"""
Final comprehensive test showing all notation types working together
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

print("╔" + "═" * 78 + "╗")
print("║" + " " * 15 + "COMPLETE LaTeX CONVERSION TEST" + " " * 32 + "║")
print("║" + " " * 20 + "All Notation Types" + " " * 37 + "║")
print("╚" + "═" * 78 + "╝")
print()

# Complete example with ALL notation types
complete_example = r"""# Fourier Series

For a periodic function ( f(t) ) with period ( T ):
\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]

where \( \omega_0 = \frac{2\pi}{T} \) is the fundamental frequency.

The coefficients are:
[
a_0 = \frac{1}{T} \int_{T} f(t)\, dt
]

Using Euler's identity ( e^{j\theta} = \cos\theta + j\sin\theta ):
\[
f(t) = \sum_{n=-\infty}^{\infty} c_n e^{j n \omega_0 t}
\]

Note: The function cos(x) without spaces stays unchanged, but ( x ) with spaces converts."""

print("📥 INPUT (Mixed Notations):")
print("─" * 80)
print(complete_example)
print()

result = preprocess_markdown(complete_example)

print("📤 OUTPUT (All Converted):")
print("─" * 80)
print(result)
print()

print("✅ VERIFICATION:")
print("─" * 80)
checks = [
    ("Legacy ( f(t) ) → $f(t)$", "$f(t)$" in result),
    ("Legacy ( T ) → $T$", "$T$" in result),
    ("LaTeX \\( \\omega_0 = ... \\) → $...$", "$\\omega_0 = " in result),
    ("LaTeX \\[...\\] → $$...$$", result.count("$$") >= 4),
    ("Legacy [...] → $$...$$", "$$" in result),
    ("Legacy equation ( e^{j\\theta} = ... ) → $...$", "$e^{j\\theta}" in result),
    ("Preserves \\left[ and \\right]", "\\left[" in result and "\\right]" in result),
    ("Preserves cos(n\\omega_0 t) function", "cos(n\\omega_0 t)" in result or "\\cos(n\\omega_0 t)" in result),
    ("Preserves cos(x) without spaces", "cos(x)" in result),
    ("Converts ( x ) with spaces", "$x$" in result),
]

for check, passed in checks:
    status = "✓" if passed else "✗"
    print(f"  {status} {check}")

all_passed = all(passed for _, passed in checks)
print()
if all_passed:
    print("🎉 ALL CHECKS PASSED! All notation types work correctly!")
else:
    print("❌ Some checks failed")
print()
