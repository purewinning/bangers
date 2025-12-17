# 🚀 Installation & Usage Instructions

## Quick Setup (5 minutes)

### Step 1: Navigate to the Project
```bash
cd dk_pro_optimizer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch the App
```bash
./run.sh
```

Or directly:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Time Usage

### Test with Sample Data
1. Launch the app
2. Click "Browse files" in the sidebar
3. Upload `sample_nfl_projections.csv`
4. Select "Balanced GPP" strategy
5. Click "Generate Optimal Lineups"
6. Review the results

### Using Your Own Data
Your CSV needs these columns:
- **Name**: Player name
- **Position**: QB, RB, WR, TE, DST (NFL) or PG, SG, SF, PF, C (NBA)
- **Team**: 3-letter abbreviation (e.g., KC, BUF)
- **Salary**: DraftKings salary (e.g., 8500)
- **Projection**: Your fantasy point projection
- **Ownership**: Projected ownership % (e.g., 15.5 for 15.5%)

Optional but recommended:
- **Game**: For NFL (e.g., "KC@BUF")

## Strategy Selection Guide

| Contest Type | Recommended Strategy | Why |
|--------------|---------------------|-----|
| Small GPP (<10K) | Balanced GPP | Can win with good chalk |
| Medium GPP (10K-50K) | Leverage Play | Need differentiation |
| Large GPP (50K-150K) | Contrarian Core | Strategic differentiation |
| Mega GPP (150K+) | Ceiling Chaser | Need tournament ceiling |
| High Stakes ($100+) | Leverage Play | Pros in these contests |

## Understanding Your Results

### Good Single-Entry Lineup
```
✅ Total Leverage: 1.0-1.2
✅ Avg Ownership: 10-15%
✅ Stack Rating: Good/Excellent
✅ Edge Plays: 3-5 identified
✅ Salary Used: 97-99%
```

### Red Flags
```
❌ Total Leverage < 0.8 (too chalky)
❌ Avg Ownership > 20% (no differentiation)
❌ No stacking/correlation
❌ All low-owned (stupid contrarian)
```

## Key Parameters Explained

### Ownership Weight (0.0 - 1.0)
- **0.5** = Equal weight to projection and ownership
- **0.7** = Moderate ownership consideration (recommended for beginners)
- **0.9** = Heavy ownership focus (for when you trust your ownership projections)

### Correlation Focus (0.0 - 1.0)
- **0.3** = Light stacking
- **0.5** = Standard stacking (recommended)
- **0.8** = Heavy stacking emphasis

### Leverage Target
- **1.0** = Ownership-neutral
- **1.1-1.2** = Moderate leverage (recommended for single-entry)
- **1.3+** = Aggressive leverage seeking

### Min Salary
- **48000** = More flexible, allows value plays
- **49000** = Forces near-full cap usage (recommended)

## Exporting Lineups

1. Generate lineups
2. Scroll to "Export Lineups"
3. Select "DraftKings CSV"
4. Click "Download DK CSV"
5. Upload directly to DraftKings

## Tips for Success

### 1. Get Good Ownership Projections
The optimizer is only as good as your inputs. Sources:
- RotoGrinders (paid, recommended)
- FantasyLabs (paid)
- Your own model
- DraftKings' projections (less accurate)

### 2. Understand Your Strategy
Read the strategy descriptions in the app. Each has specific use cases.

### 3. Don't Overthink It
- 1-3 lineups for single-entry
- Choose a strategy and stick with it
- Trust your edge

### 4. Track Your Results
Keep records:
- Contest name and size
- Strategy used
- Lineup ownership
- Finish position
- ROI

After 20+ contests, you'll see what works for you.

## Troubleshooting

### "No valid lineups generated"
- Check your projections are reasonable
- Lower min salary requirement
- Ensure salary cap accommodates your projections

### "Too chalky" warning
- Increase ownership weight
- Try Leverage Play or Contrarian Core strategy
- Check your ownership projections

### "No correlation detected"
- For NFL, ensure "Game" column is included
- Check team abbreviations are correct

### App won't start
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Advanced Features

### Multiple Strategies
Generate 1-2 lineups per strategy, then pick the best:
- Balanced GPP lineup
- Leverage Play lineup
- Compare and choose

### Custom Blends
Use "Custom Blend" and adjust parameters to create your own strategy mix.

### Slate Analysis
The app shows:
- Chalk plays (>25% ownership)
- Leverage opportunities
- Value plays
- Contrarian targets

Use this to inform your strategy selection.

## File Structure

```
dk_pro_optimizer/
├── app.py                    # Main app - run this
├── lineup_builder.py         # Optimization engine
├── strategy_engine.py        # Strategy logic
├── projection_analyzer.py    # Slate analysis
├── requirements.txt          # Dependencies
├── run.sh                    # Startup script
├── sample_nfl_projections.csv # Test data
├── README.md                 # Full documentation
├── QUICKSTART.md            # This guide
└── PROJECT_SUMMARY.md       # Project overview
```

## Next Steps

1. **Read** the full README.md for complete documentation
2. **Test** with sample_nfl_projections.csv
3. **Upload** your own projections
4. **Experiment** with different strategies
5. **Track** your results

## Support

For detailed information:
- **README.md** - Comprehensive documentation
- **PROJECT_SUMMARY.md** - Project overview and philosophy
- **Strategy info** - In the app, expand strategy details

## Remember

> "This tool doesn't give you an edge. It helps you execute your edge."

Your edge comes from:
1. Better projections than the field
2. Better ownership reads than the field  
3. Better game theory than the field

The optimizer takes your edge and builds optimal lineups around it.

**Don't be stupid contrarian. Be smart contrarian.**

Good luck! 🎯
