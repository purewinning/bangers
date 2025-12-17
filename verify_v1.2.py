#!/usr/bin/env python3
"""
Quick verification script to check if v1.2 files are correctly installed.
Run this to diagnose update issues.
"""

import sys
import os

print("=" * 60)
print("DK Pro Optimizer v1.2 - File Verification")
print("=" * 60)

# Check if projection_analyzer.py exists
if not os.path.exists('projection_analyzer.py'):
    print("❌ ERROR: projection_analyzer.py not found!")
    print("   Make sure you're in the dk_pro_optimizer directory")
    sys.exit(1)

print("\n✅ projection_analyzer.py found")

# Check the __init__ signature
print("\nChecking ProjectionAnalyzer.__init__ signature...")

with open('projection_analyzer.py', 'r') as f:
    content = f.read()
    
    # Check for the correct signature
    if 'def __init__(self, df: pd.DataFrame, sport: str, contest_type: str = None):' in content:
        print("✅ Correct v1.2 signature found:")
        print("   def __init__(self, df, sport, contest_type=None)")
    elif 'def __init__(self, df: pd.DataFrame, sport: str):' in content:
        print("❌ OLD v1.0/1.1 signature found:")
        print("   def __init__(self, df, sport)")
        print("\n🔧 FIX: Replace projection_analyzer.py with the v1.2 version")
    else:
        print("⚠️  Unknown signature - manual inspection needed")

# Check if showdown_builder.py exists (v1.2 feature)
print("\nChecking for v1.2 features...")
if os.path.exists('showdown_builder.py'):
    print("✅ showdown_builder.py found (v1.2)")
else:
    print("❌ showdown_builder.py missing")
    print("   This is required for v1.2 showdown support")

# Check app.py for contest_type
print("\nChecking app.py for contest type support...")
with open('app.py', 'r') as f:
    app_content = f.read()
    if 'contest_type' in app_content:
        print("✅ Contest type support found in app.py")
    else:
        print("❌ Contest type support missing in app.py")
        print("   You may have an old version of app.py")

print("\n" + "=" * 60)
print("Verification Complete")
print("=" * 60)

# Summary
print("\n📋 SUMMARY:")
print("If all checks pass (✅), v1.2 is correctly installed.")
print("If any checks fail (❌), replace those files with v1.2 versions.")
print("\nCommon fix: Replace projection_analyzer.py and app.py")
print("=" * 60)
