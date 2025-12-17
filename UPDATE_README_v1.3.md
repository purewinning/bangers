# DK Pro Optimizer v1.3 - Portfolio Construction System

## 🎯 What's New - Professional Portfolio Theory

v1.3 transforms the optimizer from single-lineup generation into a **professional portfolio construction system** based on how winning DFS players actually think.

### The Big Change: Portfolio > Single Lineups

**Before (v1.2):** Generate 3-5 similar lineups
**After (v1.3):** Build strategic 5-lineup portfolios with archetypes

## 🚀 New Components

### 1. Monte Carlo Simulation Engine
**File:** `monte_carlo_engine.py`

Generates 10,000+ simulations per slate to model:
- Player score distributions using projection + std dev
- Lineup finish probability
- Expected ROI calculations
- Optimal rate (how often players appear in top 1% finishes)

```python
# The Math:
Leverage = Optimal% - Ownership%

Where:
- Optimal% = Appearance rate in top 1% simulated finishes
- Ownership% = Projected field ownership  
- Positive leverage = Underowned relative to win probability
- Negative leverage = Overowned relative to results
```

### 2. Portfolio Constructor
**File:** `portfolio_constructor.py`

Builds portfolios using **5 Lineup Archetypes:**

| Archetype | Philosophy | Allocation | Target ROI |
|-----------|-----------|------------|------------|
| **Max Leverage** | Pure contrarian - maximum leverage plays | 20% (1/5) | 100-300% |
| **Balanced Leverage** | Mix of leverage + one chalk anchor | 40% (2/5) | 40-80% |
| **Correlation Hedge** | Different stacking than main thesis | 20% (1/5) | 0-40% |
| **Chalk Insurance** | Popular stacks - defensive play | 20% (1/5) | -20% to 0% |

### 3. Enhanced Projection Analyzer
**File:** `projection_analyzer.py` (UPDATED)

**Critical Fix:** Resolves the 'Ownership' column error
- Handles 30+ column name variations
- Strips hidden characters and spaces
- Better error messages showing exact columns found

**New Integrations:**
- Calculates optimal rates from simulations
- Generates correlation matrices
- Exposure management rules

## 🔧 The Ownership Column Fix

The error **"'Ownership'"** is now COMPLETELY fixed:

```python
# Now recognizes ALL these variations:
- "Ownership"
- "Own"
- "Own%"  
- "Ownership %"  ← YOUR FORMAT (with space)
- "Own %"
- "Projected Ownership"
- And more...
```

**Plus:** Strips hidden characters like `\xa0` (non-breaking spaces) that cause issues.

## 📊 How It Works

### Step 1: Simulation
```
1. Load player projections + std dev
2. Run 10,000 Monte Carlo simulations
3. Calculate score distributions for each player
4. Identify optimal rates (top 1% appearance)
```

### Step 2: Leverage Calculation
```
For each player:
- Optimal% = 15.2% (appears in 15.2% of top lineups)
- Ownership% = 8.5% (projected field ownership)
- Leverage = +6.7% (STRONG LEVERAGE PLAY)
```

### Step 3: Portfolio Construction
```
Generate 1000+ viable lineups
Classify each by sim ROI and ownership
Select 5 lineups matching archetype targets:
  1x Max Leverage (highest ROI)
  2x Balanced Leverage (repeatable edge)
  1x Correlation Hedge (different stack)
  1x Chalk Insurance (defensive)
```

### Step 4: Exposure Management
```
Calculate optimal exposure for each player:
- Leverage > 5.0 → 60% exposure (3 of 5 lineups)
- Leverage > 2.0 → 60% exposure
- Leverage > 0 → 80% exposure (4 of 5 lineups)
- Leverage < -3.0 → 20% exposure (fade but keep some)
```

## 💡 Pro's Exposure Logic Example

**Player:** Aaron Rodgers
**Projection:** 22.8
**Ownership:** 19.6%
**Optimal%:** 22.8% (from sims)
**Leverage:** +3.2%

```
Base Exposure: 60% (leverage > 2.0)
+ Elite QB bonus: +20%
= Target Exposure: 80% (4 of 5 lineups)
```

**Player:** Jaylen Waddle  
**Projection:** 12.1
**Ownership:** 18.9%
**Optimal%:** 11.2% (from sims)
**Leverage:** -7.7%

```
Base Exposure: 20% (leverage < -3.0)
No adjustments
= Target Exposure: 20% (1 of 5 lineups - fade but hedge)
```

## 🎮 What You Get

### Portfolio Dashboard View
```
┌─────────────────────────────────────────────────────────┐
│  PORTFOLIO CONSTRUCTION - NFL MAIN SLATE                │
├─────────────────────────────────────────────────────────┤
│  Lineup 1: MAX LEVERAGE                                 │
│  Sim ROI: 177%  |  Own: 34.2%  |  Duplicates: 0        │
│  Key Plays:                                             │
│  ├─ Aaron Rodgers (QB) - Leverage: +3.17%              │
│  ├─ De'Von Achane (RB) - Leverage: +2.07%              │
│  └─ Darnell Washington (TE) - Leverage: +5.40%         │
│                                                         │
│  Lineup 2: BALANCED LEVERAGE                            │
│  Sim ROI: 59.5%  |  Own: 42.3%  |  Duplicates: 2       │
│  ...                                                    │
├─────────────────────────────────────────────────────────┤
│  PORTFOLIO METRICS                                      │
│  Expected ROI: 48.3%                                    │
│  Top 1% Rate: 2.8%                                      │
│  Leverage Thesis: Rodgers + RB game script hedge       │
└─────────────────────────────────────────────────────────┘
```

### Exposure Matrix
```
PLAYER EXPOSURE ACROSS 5 LINEUPS

Player            | L1 | L2 | L3 | L4 | L5 | Total | Target
------------------|----|----|----|----|----+-------+--------
De'Von Achane     | ✓  | ✓  | ✓  | ✓  |    |  80%  |  80%  ✓
Aaron Rodgers     | ✓  |    | ✓  | ✓  |    |  60%  |  60%  ✓
Kenneth Gainwell  | ✓  | ✓  | ✓  | ✓  |    |  80%  |  80%  ✓
```

## 🔧 Installation - v1.3 Update

### What's Included
This update package contains **3 files:**

1. **projection_analyzer.py** (UPDATED) - Fixes ownership error + sim integration
2. **monte_carlo_engine.py** (NEW) - Simulation engine
3. **portfolio_constructor.py** (NEW) - Portfolio theory implementation

### How to Update

```bash
cd dk_pro_optimizer

# Add new files
# - Copy monte_carlo_engine.py
# - Copy portfolio_constructor.py

# Replace updated file
# - Replace projection_analyzer.py

# Clear Python cache
rm -rf __pycache__
find . -name "*.pyc" -delete

# Restart
streamlit run app.py
```

## ✅ What This Fixes

### The Ownership Column Error - SOLVED
```
Before: ❌ KeyError: 'Ownership'
After:  ✅ Recognizes "Ownership %", "Own %", etc.
```

**Your CSV format now works perfectly:**
```csv
Player,Salary,Position,Team,Opponent,Projection,Value,Ownership %,Optimal %,Leverage,...
```

### Plus New Features
- ✅ Monte Carlo simulations (10K+)
- ✅ Leverage calculations (optimal% - ownership%)
- ✅ Portfolio archetypes (5 lineup strategies)
- ✅ Exposure management (pro-level rules)
- ✅ Correlation matrices (QB-WR, RB-DST, etc.)

## 📚 How Pros Use This

### Example: Sunday Main Slate

**The Setup:**
- 50K entry GPP
- $20 entry
- 5 lineups to build

**The Process:**

1. **Upload CSV** with projections + ownership
2. **System runs 10K simulations** for each player
3. **Calculates leverage** (optimal% - ownership%)
4. **Generates 1000 viable lineups**
5. **Selects optimal 5-lineup portfolio**:
   - 1 max leverage (contrarian)
   - 2 balanced (core thesis)
   - 1 hedge (different stack)
   - 1 chalk (insurance)
6. **Validates exposure targets**
7. **Exports for entry**

**The Result:**
- Portfolio expected ROI: 48.3%
- Top 1% rate: 2.8%
- Proper exposure to leverage plays
- Hedged against different game scripts

## 🎯 Key Concepts

### Leverage
```
Leverage = Optimal% - Ownership%

+6.7% = STRONG LEVERAGE (underowned relative to wins)
+2.0% = GOOD LEVERAGE
 0.0% = NEUTRAL
-3.0% = POOR LEVERAGE (overowned)
-7.7% = FADE (chalk trap)
```

### Optimal Rate
```
Optimal% = Appearance rate in top 1% of simulated lineups

15.2% optimal = Player appears in 15.2% of winning lineups
 8.5% ownership = Field projects 8.5% ownership
------------------------
+6.7% leverage = EDGE OPPORTUNITY
```

### Portfolio Archetypes
```
Max Leverage    = Highest ROI, lowest own (boom or bust)
Balanced        = Repeatable edge (core thesis)
Hedge           = Different game script assumption
Chalk Insurance = Defensive (what if I'm wrong?)
```

## 🔮 Future Features (Coming Soon)

- ✅ v1.3: Portfolio construction (DONE)
- 🔄 v1.4: App UI integration with portfolio view
- 🔄 v1.5: Post-slate analysis and learning loop
- 🔄 v1.6: Historical backtesting
- 🔄 v1.7: Contest-specific payout modeling

## 📖 Documentation

- **monte_carlo_engine.py** - Documented simulation methods
- **portfolio_constructor.py** - Archetype definitions & exposure rules
- **projection_analyzer.py** - Column mapping & validation

Each file has extensive inline comments explaining the pro logic.

## ⚠️ Important Notes

### This Update Only Adds Backend
v1.3 adds the **portfolio engine** but doesn't yet integrate it into the UI.

**Current Status:**
- ✅ Portfolio system fully functional
- ✅ Can be called programmatically
- ⏳ UI integration coming in v1.4

**For Now:**
- Ownership error is FIXED
- System can be imported and used
- Full UI integration in next release

### Requirements
No new dependencies needed - uses existing:
- numpy (for simulations)
- pandas (for data handling)

## 🚀 Quick Test

After updating, test the new components:

```python
# In Python console
from monte_carlo_engine import MonteCarloEngine
from portfolio_constructor import PortfolioConstructor

# Test simulation
mc = MonteCarloEngine(num_simulations=1000)
print("Monte Carlo engine loaded ✓")

# Test portfolio
pc = PortfolioConstructor()
print(f"Portfolio archetypes: {len(pc.archetypes)} defined ✓")
```

If both print successfully, v1.3 is installed correctly!

---

**v1.3 Status:** Backend Complete, UI Integration Coming
**Ownership Error:** FIXED
**Portfolio System:** ACTIVE

Ready to build lineups like a pro! 🎯
