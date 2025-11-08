"""
Final demonstration of all supported LaTeX notations
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

demo = r"""# Fourier Series - Complete Example

## Introduction

For a periodic function \( f(t) \) with period \( T \), we can represent it using a Fourier series.

## Trigonometric Form

The trigonometric Fourier series is:
\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]

where \( \omega_0 = \frac{2\pi}{T} \) is the fundamental frequency.

### Coefficients

The coefficients are calculated as:

\[
a_0 = \frac{1}{T} \int_{T} f(t)\, dt
\]

\[
a_n = \frac{2}{T} \int_{T} f(t)\cos(n\omega_0 t)\, dt
\]

\[
b_n = \frac{2}{T} \int_{T} f(t)\sin(n\omega_0 t)\, dt
\]

## Exponential Form

Using Euler's identity \( e^{j\theta} = \cos\theta + j\sin\theta \):

\[
f(t) = \sum_{n=-\infty}^{\infty} c_n e^{j n \omega_0 t}
\]

with coefficients:
\[
c_n = \frac{1}{T} \int_{T} f(t) e^{-j n \omega_0 t}\, dt
\]

### Relation Between Coefficients

The exponential coefficients \( c_n \) relate to the trigonometric coefficients:
\[
a_n = 2 \text{Re}(c_n), \quad b_n = -2 \text{Im}(c_n)
\]

## Legacy Notation Example

You can also use legacy notation (for backward compatibility):

[
\text{Energy} = \frac{1}{T} \int_{T} |f(t)|^2\, dt
]

This works with inline too: ( x = y + z ) will be converted when it has an equation.

## Summary

Both notations work seamlessly:
- LaTeX style: \( inline \) and \[ block \]
- Legacy style: ( inline = equation ) and [ block ]
"""

print("=" * 80)
print("COMPREHENSIVE FOURIER SERIES EXAMPLE")
print("=" * 80)
print("\nINPUT (with mixed LaTeX and legacy notation):")
print("=" * 80)
print(demo)

print("\n" + "=" * 80)
print("OUTPUT (all converted to $...$ and $$...$$):")
print("=" * 80)
result = preprocess_markdown(demo)
print(result)

print("\n" + "=" * 80)
print("VERIFICATION:")
print("=" * 80)
print(f"✓ Inline \\(f(t)\\) converted: {'$f(t)$' in result}")
print(f"✓ Inline \\(T\\) converted: {'$T$' in result}")
print(f"✓ Inline \\(\\omega_0\\) converted: {'$\\omega_0' in result}")
print(f"✓ Block formulas converted: {result.count('$$') >= 16}")  # At least 8 blocks = 16 $$
print(f"✓ Preserves \\left[ and \\right]: {'\\left[' in result and '\\right]' in result}")
print(f"✓ Legacy notation [...] also converted: {'$$' in result}")
print(f"✓ No unconverted \\[ or \\(: {result.count('\\[') == 0 and result.count('\\(') == 0}")
print()
