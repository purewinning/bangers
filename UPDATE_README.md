# DK Pro Optimizer v1.2 - Update Package

## 🎯 What's New

### Showdown/Captain Mode Support
✅ Full optimization for DraftKings Showdown contests
✅ Captain selection (1.5x points, 1.5x salary)
✅ CPT-specific ownership and leverage
✅ 1 CPT + 5 FLEX roster construction

### Enhanced CSV Format Support
✅ Your exact format now fully supported:
```csv
Player,Salary,Position,Team,Opponent,Projection,Value,Ownership %,Optimal %,Leverage,CPT Ownership %,CPT Optimal %,CPT Leverage,Std Dev
```

✅ Recognizes 30+ column name variations
✅ Auto-calculates missing metrics
✅ Uses Std Dev for better ceiling calculations

## 📦 Files in This Update

### New Files (Add These):
1. **showdown_builder.py** - Showdown optimization engine
2. **sample_showdown_projections.csv** - Example showdown data
3. **SHOWDOWN_GUIDE.md** - Complete showdown documentation

### Updated Files (Replace These):
4. **app.py** - Added contest type selection & showdown support
5. **projection_analyzer.py** - Enhanced column mapping & detection
6. **CHANGELOG.md** - Version history

## 🔧 How to Update

### Option 1: Add New Files + Replace Updated Files

```bash
cd dk_pro_optimizer

# Add new files
# - Copy showdown_builder.py to main folder
# - Copy sample_showdown_projections.csv to main folder
# - Copy SHOWDOWN_GUIDE.md to main folder

# Replace these 3 files
# - Replace app.py
# - Replace projection_analyzer.py
# - Replace CHANGELOG.md
```

### Option 2: Fresh Install
If you haven't customized anything, download the full v1.2 package.

## ✅ What This Fixes & Adds

### Your CSV Format - Now Works!
```csv
Player,Salary,Position,Team,Opponent,Projection,Value,Ownership %,Optimal %,Leverage,CPT Ownership %,CPT Optimal %,CPT Leverage,Std Dev
Patrick Mahomes,11400,QB,KC,BUF,23.5,2.06,32.5,28.3,0.72,45.2,38.1,0.78,6.2
```

**Before v1.2:** ❌ Columns not recognized
**After v1.2:** ✅ Fully supported, all variations mapped

### Showdown Mode
```
Before: Only classic DFS (QB/RB/WR/TE/DST)
After: Classic + Showdown (1 CPT + 5 FLEX)
```

### Auto-Calculations
Even if your CSV is missing columns:
- ✅ Value → Calculated from Projection/Salary
- ✅ Leverage → Calculated from Projection/Ownership
- ✅ Ceiling → Calculated from Projection + (1.5 × Std Dev)
- ✅ CPT metrics → Calculated if missing

## 🎮 Testing the Update

### Test Classic Mode
1. Upload: `sample_nfl_projections.csv` (original file)
2. Contest Type: Classic
3. Should work exactly as before

### Test Showdown Mode
1. Upload: `sample_showdown_projections.csv` (new file)
2. Contest Type: Auto-detected as Showdown
3. Generate lineups with captain optimization

### Test Your Format
1. Upload: Your CSV with "Player", "Ownership %", etc.
2. Should auto-map all columns
3. All features work perfectly

## 🔍 What Changed in Each File

### app.py
- Added `contest_type` selection dropdown
- Imported `ShowdownLineupBuilder`
- Added showdown vs classic detection display
- Updated lineup display for captain/role
- Added support for optional columns (Opponent, Optimal, StdDev)

### projection_analyzer.py
- Enhanced column mapping (30+ variations)
- Added contest type detection
- Auto-calculates CPT metrics
- Uses Std Dev for ceiling if available
- Handles "Player" vs "Name" column

### showdown_builder.py (NEW)
- Complete showdown optimization engine
- Captain selection strategies
- CPT leverage weighting
- FLEX player optimization
- Showdown-specific analytics

## 📊 Backwards Compatibility

✅ **100% compatible with v1.0 and v1.1**
- Original CSV format still works
- All classic strategies unchanged
- No breaking changes
- Can safely update

## 📚 Documentation

Read **SHOWDOWN_GUIDE.md** for:
- Complete showdown strategy guide
- CSV format examples
- Captain selection tips
- Showdown vs Classic comparison
- Troubleshooting

## ⚡ Quick Start After Update

```bash
# Classic contest
Contest Type: Classic
Upload: sample_nfl_projections.csv
Strategy: Balanced GPP
Generate lineups ✓

# Showdown contest  
Contest Type: Showdown
Upload: sample_showdown_projections.csv
Strategy: Leverage Play
Generate lineups ✓
```

## 🎯 Key Benefits

1. **Works with your data** - No need to reformat CSVs
2. **Showdown optimization** - Captain mode fully supported
3. **Smarter calculations** - Uses Std Dev for better ceilings
4. **Auto-detection** - Knows classic vs showdown automatically
5. **More flexibility** - Recognizes any reasonable column name

## ❓ Questions?

- **Do I need all these files?** Yes, for full v1.2 features
- **Will my old CSVs work?** Yes, 100% backwards compatible
- **Can I mix classic and showdown?** Yes, switch via dropdown
- **Is showdown required?** No, classic mode still works great

---

**Enjoy the new Showdown mode and enhanced CSV support!** 🚀

**Version:** 1.2
**Date:** December 2024
**Status:** Production Ready
