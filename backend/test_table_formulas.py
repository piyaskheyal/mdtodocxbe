#!/usr/bin/env python3
"""
Test table with formulas
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

test = """Classification based on the discriminant ( B^2 - 4AC ):

| Type       | Condition         | Example            |
| ---------- | ----------------- | ------------------ |
| Elliptic   | ( B^2 - 4AC < 0 ) | Laplace's equation |
| Parabolic  | ( B^2 - 4AC = 0 ) | Heat equation      |
| Hyperbolic | ( B^2 - 4AC > 0 ) | Wave equation      |
"""

print("=" * 80)
print("TEST: Table with formulas in parentheses")
print("=" * 80)
print("\nINPUT:")
print(test)

result = preprocess_markdown(test)

print("\nOUTPUT:")
print(result)

expected = """Classification based on the discriminant $B^2 - 4AC$:

| Type       | Condition         | Example            |
| ---------- | ----------------- | ------------------ |
| Elliptic   | $B^2 - 4AC < 0$ | Laplace's equation |
| Parabolic  | $B^2 - 4AC = 0$ | Heat equation      |
| Hyperbolic | $B^2 - 4AC > 0$ | Wave equation      |
"""

print("\nEXPECTED:")
print(expected)

print("\nVERIFICATION:")
print(f"  First line converted: {'$B^2 - 4AC$:' in result}")
print(f"  Table row 1: {'$B^2 - 4AC < 0$' in result}")
print(f"  Table row 2: {'$B^2 - 4AC = 0$' in result}")
print(f"  Table row 3: {'$B^2 - 4AC > 0$' in result}")
print(f"  All formulas converted: {result.count('$') == 8}")  # 4 formulas × 2 delimiters
