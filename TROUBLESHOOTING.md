# Troubleshooting: "takes 3 positional arguments but 4 were given"

## The Problem

You're seeing this error:
```
❌ Error Processing File
ProjectionAnalyzer.__init__() takes 3 positional arguments but 4 were given
```

## What This Means

You have a **version mismatch** - the `app.py` file is v1.2 but `projection_analyzer.py` is still v1.0/v1.1.

### Version Comparison:

**v1.0/v1.1 (OLD):**
```python
def __init__(self, df: pd.DataFrame, sport: str):
    # Takes 2 arguments (+ self = 3 total)
```

**v1.2 (NEW):**
```python
def __init__(self, df: pd.DataFrame, sport: str, contest_type: str = None):
    # Takes 3 arguments (+ self = 4 total)
```

## Quick Fix

You need to replace **both** `app.py` AND `projection_analyzer.py` together.

### Step 1: Verify Your Files

```bash
# Navigate to your optimizer folder
cd dk_pro_optimizer

# Run verification script
python verify_v1.2.py
```

This will tell you which files are outdated.

### Step 2: Replace Files

From the v1.2 update package, replace these files:

✅ **projection_analyzer.py** - CRITICAL (must update)
✅ **app.py** - CRITICAL (must update)
✅ **showdown_builder.py** - NEW FILE (add this)

These files work together and must all be v1.2.

### Step 3: Restart the App

```bash
# Stop the current app (Ctrl+C)
# Restart it
streamlit run app.py
```

## Detailed Fix Steps

### If You Updated Manually:

1. **Delete old files:**
   ```bash
   rm app.py
   rm projection_analyzer.py
   ```

2. **Copy new files from update package:**
   - Copy `app.py` from v1.2 update
   - Copy `projection_analyzer.py` from v1.2 update
   - Copy `showdown_builder.py` from v1.2 update (new file)

3. **Restart:**
   ```bash
   streamlit run app.py
   ```

### If You're Using Python Cache:

Python might be using cached `.pyc` files. Clear them:

```bash
# In your dk_pro_optimizer folder
find . -type d -name __pycache__ -exec rm -rf {} +
rm -f *.pyc

# Then restart
streamlit run app.py
```

## Verify It's Fixed

After updating, the app should:

1. Show "Contest Type" dropdown in sidebar
2. Have options: "Classic" and "Showdown"
3. Load your CSV without errors
4. Auto-detect contest type

## Alternative: Fresh Install

If issues persist, do a fresh install:

1. **Backup your custom files** (if you made any changes)
2. **Delete the entire folder:**
   ```bash
   rm -rf dk_pro_optimizer
   ```
3. **Extract the FULL v1.2 package:**
   - Unzip `DK_Pro_Optimizer_v1.2_FULL.zip`
4. **Install and run:**
   ```bash
   cd dk_pro_optimizer
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Still Having Issues?

### Check Python Cache

```bash
# Clear all Python cache
cd dk_pro_optimizer
rm -rf __pycache__
find . -name "*.pyc" -delete
```

### Check File Versions

Run this in your dk_pro_optimizer folder:

```python
# Check projection_analyzer.py
grep "def __init__" projection_analyzer.py

# Should show:
# def __init__(self, df: pd.DataFrame, sport: str, contest_type: str = None):
```

If it doesn't show `contest_type`, your file is outdated.

### Verify All v1.2 Files Are Present

```bash
ls -la

# Should include:
# - app.py (modified date recent)
# - projection_analyzer.py (modified date recent)  
# - showdown_builder.py (NEW - if missing, you don't have v1.2)
# - sample_showdown_projections.csv (NEW)
# - SHOWDOWN_GUIDE.md (NEW)
```

## Prevention

When updating in the future:

1. ✅ **Replace ALL files** listed in UPDATE_README.md
2. ✅ **Clear Python cache** after updating
3. ✅ **Restart the app** completely (don't just refresh browser)
4. ✅ **Check version numbers** match

## Quick Checklist

- [ ] `projection_analyzer.py` has `contest_type` parameter
- [ ] `app.py` has "Contest Type" dropdown
- [ ] `showdown_builder.py` exists
- [ ] Python cache cleared (`__pycache__` deleted)
- [ ] App restarted (not just browser refresh)

If all checked, it should work!

---

**TL;DR: Replace both `app.py` AND `projection_analyzer.py` together, clear cache, restart app.**
