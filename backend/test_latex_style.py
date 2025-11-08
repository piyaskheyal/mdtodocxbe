"""
Test LaTeX-style delimiters \(...\) and \[...\]
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

# Test 1: LaTeX inline math \( ... \)
test1 = r"""For a periodic function \( f(t) \) with period \( T \):
\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]"""

print("=" * 80)
print("TEST 1: LaTeX-style delimiters \\(...\\) and \\[...\\]")
print("=" * 80)
print("INPUT:")
print(test1)
print("\nOUTPUT:")
result1 = preprocess_markdown(test1)
print(result1)
print("\nVERIFICATION:")
print(f"  Inline \\(f(t)\\) converted to $f(t)$: {'$f(t)$' in result1}")
print(f"  Inline \\(T\\) converted to $T$: {'$T$' in result1}")
print(f"  Block \\[...\\] converted to $$...$$: {'$$' in result1}")
print(f"  Preserves \\left[ and \\right]: {'\\left[' in result1 and '\\right]' in result1}")
print()

# Test 2: ChatGPT example
test2 = r"""Good catch — here's the deal:

I use **LaTeX math rendering inside Markdown**, but the delimiters are slightly different from what you'd use in plain Markdown files.

* **Inline math:** I use `\( ... \)`
  → Example: \( f(t) = \sin(\omega t) \)

* **Block (display) math:** I use `\[ ... \]`
  → Example:
  \[
  a_n = \frac{2}{T} \int_{T} f(t) \cos(n\omega_0 t), dt
  \]

So instead of `$...$` and `$$...$$`, I use `\(...\)` and `\[...\]`."""

print("=" * 80)
print("TEST 2: ChatGPT's actual example")
print("=" * 80)
print("INPUT:")
print(test2)
print("\nOUTPUT:")
result2 = preprocess_markdown(test2)
print(result2)
print()

# Test 3: Mixed notation (both old [...] and new \[...\])
test3 = r"""# Mixed Notation Test

Using old style:
[
a_0 = \frac{1}{T} \int_{T} f(t), dt
]

Using LaTeX style:
\[
b_0 = \frac{2}{T} \int_{T} g(t), dt
\]

Inline old: ( e^{j\theta} = \cos\theta )
Inline LaTeX: \( e^{-j\theta} = \cos\theta - j\sin\theta \)"""

print("=" * 80)
print("TEST 3: Mixed notation (both old and LaTeX style)")
print("=" * 80)
print("INPUT:")
print(test3)
print("\nOUTPUT:")
result3 = preprocess_markdown(test3)
print(result3)
print("\nVERIFICATION:")
print(f"  Old style [...] converted: {result3.count('$$') >= 2}")
print(f"  LaTeX style \\[...\\] converted: {'$$' in result3}")
print(f"  Old inline (...) converted: {'$e^{j\\theta}' in result3}")
print(f"  LaTeX inline \\(...\\) converted: {'$e^{-j\\theta}' in result3}")
print()

# Test 4: Real-world example from user
test4 = r"""For a periodic function \( f(t) \) with period \( T \):
\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right]
\]

where the coefficients are:
\[
a_0 = \frac{1}{T} \int_{T} f(t), dt
\]
\[
a_n = \frac{2}{T} \int_{T} f(t)\cos(n\omega_0 t), dt
\]
\[
b_n = \frac{2}{T} \int_{T} f(t)\sin(n\omega_0 t), dt
\]"""

print("=" * 80)
print("TEST 4: Real-world example with inline variables")
print("=" * 80)
print("INPUT:")
print(test4)
print("\nOUTPUT:")
result4 = preprocess_markdown(test4)
print(result4)
print("\nVERIFICATION:")
print(f"  \\(f(t)\\) → $f(t)$: {'$f(t)$' in result4}")
print(f"  \\(T\\) → $T$: {'$T$' in result4}")
print(f"  All block formulas converted: {result4.count('$$') >= 8}")  # 4 blocks = 8 $$
print()

print("=" * 80)
print("✅ ALL TESTS COMPLETED")
print("=" * 80)
