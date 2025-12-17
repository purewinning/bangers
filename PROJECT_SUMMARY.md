# DraftKings Pro Tournament Optimizer - Project Summary

## What I Built

A professional-grade DFS lineup optimizer specifically designed for **single-entry, high-stakes tournament play** against experienced competition. This isn't your typical "mass multi-entry" optimizer or beginner tool - it's built around the strategies that professional players use to win large-field GPPs.

## Core Philosophy

**"Don't be stupid contrarian. Be smart contrarian."**

The optimizer focuses on:
- ✅ Strategic leverage (projection-to-ownership ratio)
- ✅ Smart correlation and game stacking
- ✅ Context-aware ownership targets
- ✅ Professional build patterns
- ❌ NOT mass multi-entry (MME)
- ❌ NOT blindly contrarian
- ❌ NOT generic "optimal" lineups

## Key Features

### 6 Professional Strategies

1. **Balanced GPP** - Workhorse strategy (10-15% avg ownership)
2. **Leverage Play** - Exploit ownership inefficiencies (8-12% avg ownership)
3. **Contrarian Core** - Smart differentiation (7-10% avg ownership)
4. **Ceiling Chaser** - Pure upside plays for massive tournaments
5. **Correlation Stack** - Game-based correlation maximization
6. **Custom Blend** - Adaptive strategy mixing

Each strategy includes:
- Detailed philosophy and principles
- Target ownership distributions
- Risk assessment
- Best use cases
- Sport-specific tactics

### Advanced Analytics

**Lineup Metrics:**
- Total leverage ratio
- Ceiling score (90th percentile)
- Stack quality rating
- Construction notes
- Edge play identification

**Slate Analysis:**
- Ownership distribution breakdown
- Leverage opportunity identification
- Value play detection
- Contrarian target analysis
- Correlation matrices

### Professional Stacking Logic

**NFL:**
- Primary stacks (QB + pass catchers)
- Bring-back strategies (opposing team)
- Full game stacks (high total games)
- Negative correlation avoidance (RB + DST)

**NBA:**
- Team stacks (2-3 optimal)
- High-pace game targeting
- Opposing star shootouts
- Blowout fade strategies

## How It Works

### 1. Data Input
Upload CSV with projections and ownership:
```
Name, Position, Team, Salary, Projection, Ownership
```

### 2. Strategy Selection
Choose based on:
- Contest size (10K vs 150K entries)
- Entry fee ($20 vs $500)
- Your edge/information
- Risk tolerance

### 3. Parameter Tuning
- **Ownership Weight:** How much to consider ownership vs projections
- **Correlation Focus:** Stack strength emphasis
- **Leverage Target:** Desired proj/ownership ratio
- **Min Salary:** Cap utilization target

### 4. Optimization Engine
The lineup builder:
- Calculates optimal scores (not just raw projection)
- Implements strategy-specific player selection
- Enforces correlation rules
- Validates position requirements
- Avoids chalk traps

### 5. Output & Analysis
For each lineup:
- Full player roster with analytics
- Construction notes ("4 low-owned plays for differentiation")
- Edge identification ("Player X: High leverage 1.85")
- Stack quality assessment
- DraftKings-ready CSV export

## Technical Architecture

```
app.py (Streamlit UI)
├── lineup_builder.py (Core optimization logic)
│   ├── Position filling algorithm
│   ├── Strategy-specific scoring
│   ├── Stack bonus calculations
│   └── Lineup validation
│
├── strategy_engine.py (Strategy definitions)
│   ├── 6 professional strategies
│   ├── Ownership targets
│   ├── Sport-specific tactics
│   └── Validation rules
│
└── projection_analyzer.py (Slate analysis)
    ├── Leverage calculations
    ├── Value identification
    ├── Chalk detection
    └── Stack opportunity analysis
```

## What Makes This Different

### vs. Basic Optimizers
- **They:** Maximize raw projection
- **This:** Maximizes tournament-winning probability considering ownership

### vs. MME Optimizers  
- **They:** Generate 150 lineups for every angle
- **This:** Generate 1-3 highly strategic single-entry lineups

### vs. Generic Contrarian Tools
- **They:** Fade all chalk indiscriminately
- **This:** Strategic differentiation at leverage spots

## The Edge Framework

Success in DFS comes from having at least ONE of these edges:

1. **Better Projections**
   - Your model > field's projections
   - Better injury/usage forecasts
   - Superior game script modeling

2. **Better Ownership Reads**
   - Field overreacts to narratives
   - You identify chalk traps
   - You find overlooked leverage

3. **Better Game Theory**
   - Strategic position differentiation
   - Smart correlation usage
   - Optimal ownership distribution

This tool helps you **execute** your edge, it doesn't give you the edge itself.

## Real-World Application

### Example: Sunday Main Slate NFL

**The Slate:**
- Patrick Mahomes: 28% ownership, 24.5 proj
- Tyreek Hill: 38% ownership, 22.4 proj
- Christian McCaffrey: 45% ownership, 26.8 proj

**The Strategy: Leverage Play**

**The Build:**
- Mahomes at 28% ✅ (leverage 0.88, but elite QB)
- Fade Tyreek at 38% ❌ (leverage 0.59, chalk trap)
- CMC at 45% ✅ (too good to fade, anchor play)
- Add: Mid-tier QB at 8% ownership with 20+ proj (leverage 2.5+)
- Stack: QB's pass catchers at 12-15% ownership
- Bring-back: Opposing RB at 9% ownership

**Result:** 13.2% average ownership, 1.18 total leverage, strong correlation

### Why This Wins

1. **Not totally contrarian** (kept CMC, Mahomes)
2. **Strategic differentiation** (faded Tyreek for leverage play)
3. **Smart stacking** (QB correlation with low-owned pieces)
4. **Proper ownership distribution** (not all chalk, not all punts)

## Files Included

```
dk_pro_optimizer/
├── app.py                          # Main Streamlit application
├── lineup_builder.py               # Core optimization engine
├── strategy_engine.py              # Strategy definitions & logic
├── projection_analyzer.py          # Slate analysis tools
├── requirements.txt                # Python dependencies
├── run.sh                          # Startup script
├── README.md                       # Comprehensive documentation
├── QUICKSTART.md                   # Quick start guide
├── sample_nfl_projections.csv      # Example data
└── PROJECT_SUMMARY.md              # This file
```

## Getting Started

### Installation
```bash
cd dk_pro_optimizer
pip install -r requirements.txt
```

### Run
```bash
./run.sh
# or
streamlit run app.py
```

### First Steps
1. Upload `sample_nfl_projections.csv` to test
2. Try "Balanced GPP" strategy
3. Generate 3 lineups
4. Review the analytics
5. Upload your own projections with ownership data

## Advanced Usage

### Custom Strategy Development
Edit `strategy_engine.py` to add your own strategies based on what you observe in winning lineups.

### Projection Integration
The optimizer accepts any CSV format. Integrate with:
- Your own projection models
- RotoGrinders API
- FantasyLabs data
- Consensus projections

### Parameter Optimization
Track your results and adjust:
- Which strategies work best for you
- Optimal ownership weights
- Leverage targets by contest size

## Key Takeaways

1. **Leverage is King**
   - Projection/Ownership ratio drives tournament success
   - Target 1.0-1.2 overall leverage for single-entry

2. **Correlation Matters**
   - Proper stacking amplifies upside
   - Avoid negative correlations (RB + DST)

3. **Strategic Ownership**
   - 2-3 chalk anchors
   - 3-4 medium-owned value plays
   - 2-3 low-owned differentiation pieces

4. **Not All Contrarian is Equal**
   - Smart contrarian: Overlooked player in good spot
   - Stupid contrarian: Punt play in terrible matchup

5. **Context Over Metrics**
   - 6x value in a blowout = bad
   - 4x value in a shootout = good
   - Always consider game script

## Limitations & Future Enhancements

### Current Limitations
- NBA optimization simplified (needs full multi-position logic)
- Correlation based on theoretical values (needs historical data)
- No live ownership tracking
- No contest-specific features (Milly vs regular GPP)

### Future Enhancements
- Historical winning lineup analysis
- Real correlation matrices from game data
- Live ownership updates
- Showdown slate optimizer
- Multi-slate bankroll management
- ROI tracking dashboard

## Philosophy Reminder

**This tool doesn't give you an edge. It helps you execute your edge.**

Your edge comes from:
- Better information (projections, ownership, news)
- Better analysis (game theory, leverage spots)
- Better decision-making (strategic differentiation)

The optimizer takes your edge and builds optimal lineups around it.

---

## Final Thoughts

DFS success at high stakes requires:
1. **Information edge** (better projections/ownership reads)
2. **Strategic execution** (proper build patterns)
3. **Bankroll management** (variance is high)
4. **Continuous learning** (field adapts, you must too)

This optimizer handles #2. You need to provide #1 and practice #3 and #4.

**Don't be stupid contrarian. Be smart contrarian.**

Good luck!
