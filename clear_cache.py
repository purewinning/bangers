#!/usr/bin/env python3
"""
Clear ALL Python cache and force reload
"""

import os
import sys
import shutil

print("=" * 60)
print("CLEARING PYTHON CACHE")
print("=" * 60)

cache_cleared = False

# Clear __pycache__ directories
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        print(f"Removing: {cache_dir}")
        shutil.rmtree(cache_dir)
        cache_cleared = True

# Clear .pyc files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            pyc_file = os.path.join(root, file)
            print(f"Removing: {pyc_file}")
            os.remove(pyc_file)
            cache_cleared = True

# Clear .streamlit cache if it exists
if os.path.exists('.streamlit'):
    print("Clearing .streamlit cache...")
    for item in os.listdir('.streamlit'):
        if item != 'config.toml':  # Keep config
            item_path = os.path.join('.streamlit', item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            cache_cleared = True

if cache_cleared:
    print("\n✅ Cache cleared successfully!")
else:
    print("\nℹ️ No cache found (already clean)")

print("\n" + "=" * 60)
print("CACHE CLEAR COMPLETE")
print("=" * 60)
print("\nNow restart the app:")
print("  streamlit run app.py")
print("=" * 60)
