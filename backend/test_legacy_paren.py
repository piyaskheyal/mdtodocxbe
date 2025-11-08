#!/usr/bin/env python3
"""
Test the legacy notation with spaces: ( var )
"""
import sys
sys.path.insert(0, '/home/kheyal/dev/mdtodocxbe/backend')

from utils.markdown_processor import preprocess_markdown

print("=" * 80)
print("TEST: Legacy notation ( var ) with spaces")
print("=" * 80)

# Your exact example
test = """For a periodic function ( f(t) ) with period ( T ):\n"""

print("\nINPUT:")
print(test)

result = preprocess_markdown(test)

print("OUTPUT:")
print(result)

print("\nEXPECTED:")
print("For a periodic function $f(t)$ with period $T$:")

print("\nVERIFICATION:")
print(f"  ( f(t) ) → $f(t)$: {'$f(t)$' in result}")
print(f"  ( T ) → $T$: {'$T$' in result}")
print(f"  Match expected: {result.strip() == 'For a periodic function $f(t)$ with period $T$:'}")
