# Changelog

## Version 1.2 - Showdown Mode & Enhanced CSV Support

### 🎯 New Features

1. **Showdown/Captain Mode** ✅
   - Full support for DraftKings Showdown contests
   - Captain selection optimization (1.5x points, 1.5x salary)
   - CPT-specific ownership and leverage calculations
   - 1 CPT + 5 FLEX roster construction
   - Showdown-specific strategies and analytics
   - Auto-detection of showdown vs classic contests

2. **Enhanced CSV Format Support** ✅
   - Recognizes 30+ column name variations
   - Supports your exact format: "Player, Salary, Position, Team, Opponent, Projection, Value, Ownership %, Optimal %, Leverage, CPT Ownership %, CPT Optimal %, CPT Leverage, Std Dev"
   - Auto-calculates missing columns (Value, Leverage, Ceiling)
   - Uses provided Std Dev for better ceiling calculations
   - CPT columns for showdown ownership projections

3. **Intelligent Column Mapping** ✅
   - Recognizes "Player" as "Name"
   - Recognizes "Ownership %" as "Ownership"
   - Handles spaces in column names
   - Case-insensitive matching
   - Preserves your calculated values if provided

4. **Contest Type Selection** ✅
   - Manual selection: Classic or Showdown
   - Auto-detection based on CPT columns
   - Contest-specific optimization logic
   - Proper display formatting for each type

### 📦 New Files

- `showdown_builder.py` - Showdown lineup optimization engine
- `sample_showdown_projections.csv` - Example showdown data
- `SHOWDOWN_GUIDE.md` - Complete showdown documentation

### 🔧 Updated Files

- `projection_analyzer.py` - Enhanced column mapping, showdown detection
- `app.py` - Contest type selection, showdown builder integration
- `CHANGELOG.md` - This file

### 💡 Key Improvements

**Better CSV Compatibility:**
```csv
# Your format - now fully supported!
Player,Salary,Position,Team,Opponent,Projection,Value,Ownership %,Optimal %,Leverage,CPT Ownership %,CPT Optimal %,CPT Leverage,Std Dev
```

**Showdown Optimization:**
- Captain leverage weighted heavily
- CPT vs FLEX ownership dynamics
- Single-game correlation built-in
- Showdown-specific construction notes

**Auto-Calculations:**
- Missing Value? Calculated from Proj/Salary
- Missing Leverage? Calculated from Proj/Own
- Missing CPT columns? Calculated automatically
- Missing Ceiling? Calculated from Proj + (1.5 × Std Dev)

### 📊 Example Improvements

**Before v1.2:**
```
❌ "Ownership %" not recognized
❌ No showdown support
❌ Manual value calculations required
```

**After v1.2:**
```
✅ "Ownership %" auto-mapped to "Ownership"
✅ Full showdown/captain mode
✅ All metrics auto-calculated if missing
✅ CPT leverage optimization
```

### 🎮 Usage

**Classic Contests:**
```bash
Contest Type: Classic
Upload: sample_nfl_projections.csv or your enhanced format
Generate lineups with traditional stacking
```

**Showdown Contests:**
```bash
Contest Type: Showdown (or auto-detected)
Upload: sample_showdown_projections.csv or your format
Generate lineups with captain optimization
```

### 🐛 Compatibility

- ✅ Backwards compatible with original CSV format
- ✅ Works with enhanced format from projection tools
- ✅ Auto-detects contest type from data
- ✅ Preserves all v1.1 bug fixes

---

## Version 1.1 - Bug Fixes

### Issues Fixed

1. **Missing Column Error** ✅
   - **Problem:** App crashed when CSV was missing required columns
   - **Fix:** Added intelligent column mapping for common variations
   - **Result:** Auto-maps "Sal" to "Salary", "Proj" to "Projection", etc.

2. **Better Error Messages** ✅
   - **Problem:** Generic errors didn't tell users what was wrong
   - **Fix:** Added try-except blocks with specific error messages
   - Shows exactly which columns are missing
   - Lists columns found in CSV
   - Provides quick fix suggestions

3. **Column Display** ✅
   - **Problem:** App tried to display columns that didn't exist
   - **Fix:** Added column existence checks before displaying
   - Only shows columns actually present in data

### Files Modified

- `app.py` - Added error handling and column detection
- `projection_analyzer.py` - Added intelligent column mapping

---

## Version 1.0 - Initial Release

- 6 professional tournament strategies
- Classic DFS optimization (QB/RB/WR/TE/DST)
- Leverage and correlation analysis
- NFL game stacking
- Value and ownership optimization
- DraftKings CSV export

---

**Current Version: 1.2**
**Last Updated: December 2024**
