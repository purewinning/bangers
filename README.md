# DraftKings Pro Tournament Optimizer

A professional-grade DFS lineup optimizer focused on winning single-entry tournaments against experienced competition. Built for players who compete in high-stakes contests where edge-finding and strategic differentiation matter.

## 🎯 Philosophy

This optimizer is **NOT** for:
- Mass multi-entry (MME) strategies
- Beginners looking for simple "optimal" lineups
- Cash game optimization
- Mindless contrarian plays

This optimizer **IS** for:
- Single-entry tournament players
- High-stakes contests ($100+ buy-ins)
- Players who understand leverage and ownership
- Strategic differentiation without being stupidly contrarian

## 🧠 Core Strategies

### 1. Balanced GPP
The workhorse strategy for most tournaments. Mix of chalk and leverage plays.
- **Target Ownership:** 10-15% average
- **Use Case:** Main slate single-entry tournaments
- **Philosophy:** Be different where it matters, not everywhere

### 2. Leverage Play
Exploit projection-to-ownership inefficiencies.
- **Target Ownership:** 8-12% average
- **Use Case:** When you have strong ownership projections
- **Philosophy:** The field is wrong on certain players - capitalize on it

### 3. Contrarian Core
Strategic differentiation without being reckless.
- **Target Ownership:** 7-10% average
- **Use Case:** Massive field tournaments (100K+ entries)
- **Philosophy:** 3-5 low-owned plays with legitimate upside, not 8-9 punts

### 4. Ceiling Chaser
Tournament-winning ceiling over safety floor.
- **Target Ownership:** 12-18% average (mix of chalk and ceiling plays)
- **Use Case:** Sunday Million, Milly Maker contests
- **Philosophy:** Min-cash doesn't matter. Build for top 0.1%

### 5. Correlation Stack
Maximize correlated plays from high-total games.
- **Target Ownership:** Varies by game popularity
- **Use Case:** High over/under games with leverage
- **Philosophy:** When one piece hits, multiple pieces hit together

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `localhost:8501`.

### Using the App

1. **Upload Projections**
   - CSV must include: Name, Position, Team, Salary, Projection, Ownership
   - Ownership should be in percentage format (15.5 for 15.5%)
   - For NFL, include "Game" column (e.g., "DAL@NYG")

2. **Select Strategy**
   - Choose based on contest size and your edge
   - Each strategy has detailed info in the app

3. **Adjust Parameters**
   - **Ownership Weight:** How much to consider ownership vs raw projections
   - **Correlation Focus:** Stack strength emphasis
   - **Leverage Target:** Desired projection/ownership ratio
   - **Min Salary:** Avoid leaving too much money on the table

4. **Generate Lineups**
   - Review lineup analytics (leverage, ceiling, stack quality)
   - Check construction notes and edge plays
   - Export for DraftKings upload

## 📊 Key Metrics Explained

### Leverage
```
Leverage = Projection / Ownership
```
- **1.0** = Ownership-neutral (projection matches ownership)
- **>1.5** = High leverage (underowned relative to projection)
- **<0.7** = Poor leverage (overowned relative to projection)

Target leverage ratios:
- Single-entry GPP: 1.0-1.2
- Leverage strategy: 1.2-1.5
- Avoid: <0.8 (chalk trap)

### Value
```
Value = Projection / (Salary / 1000)
```
- **>1.0** = Strong value
- **0.8-1.0** = Fair value
- **<0.8** = Poor value

### Ceiling Score
90th percentile projection - what the player scores when everything goes right.

## 🏈 NFL Stacking Theory

### Primary Stack
- **QB + WR/TE** from same team
- Highest correlation in DFS
- Target 1-2 pass catchers with your QB

### Bring-Back
- Opposing RB or WR from same game
- Hedges QB stack
- Critical for single-entry success

### Full Game Stack
- QB + 2 pass catchers + opposing skill player
- For high over/under games
- High ceiling, high variance

### What to Avoid
- **RB + DST** same team (negative correlation)
- **Over-stacking** (4+ players from one team)
- **Chalky stacks** everyone is playing

## 🏀 NBA Stacking Theory

### Team Stacks
- **2-3 players** from high-pace teams
- Optimal: 3 players
- Avoid: 4+ players (over-concentration)

### Opposing Stars
- Stars from both teams in potential shootout
- Pace-up game environments

### Value Plays
- Increased minutes due to injury
- Late scratch leverage

## 📈 Ownership Strategy

### Professional Build Pattern
```
Chalk (>25% ownership):    2-3 players
Medium (10-25% ownership): 3-4 players  
Low (<10% ownership):      2-3 players
```

**Not this:**
```
Chalk:    0-1 players (too contrarian)
Low-own:  6-7 players (stupidly contrarian)
```

### Leverage Spots

**Good leverage spots:**
- Mid-tier QBs in good matchups
- WR2s with WR1 volume
- Overlooked RBs in good game scripts
- Value TEs in pass-heavy games

**Bad leverage spots:**
- DST (rarely matters)
- Backup RBs with no clear path to touches
- Players in negative game scripts

## 💡 Advanced Concepts

### Implied Leverage
Even if your lineup has 1.1 overall leverage, the **distribution** matters:
- ✅ 4 players at 1.5+ leverage, 5 at 0.9-1.1
- ❌ All 9 players at exactly 1.1

### Tournament Theory
In large-field GPPs:
- You need **one** lineup to bink, not 20 to min-cash
- Ceiling > Floor
- Differentiate at expensive positions (QB, RB, WR)
- Being different at DST doesn't matter much

### Chalk Traps
Avoid players with:
- High ownership (>30%)
- Negative game script projection
- Touchdown dependency without volume
- Popular but not actually optimal

### Smart Contrarian
**Good contrarian:**
- Low-owned player in good game environment
- Overlooked due to recency bias
- Value play field is fading

**Bad contrarian:**
- Cheap player in horrible matchup
- Contrarian just to be different
- Ignoring obvious優 plays

## 🛠️ Customization

### Adding Your Own Projections
The optimizer works with any CSV format. Just map your columns:
```python
# In projection_analyzer.py, adjust column mapping
df.rename(columns={
    'YourProjectionCol': 'Projection',
    'YourOwnershipCol': 'Ownership'
}, inplace=True)
```

### Adjusting Strategy Parameters
Edit `strategy_engine.py` to customize:
- Ownership targets
- Leverage thresholds
- Correlation weights
- Stack preferences

### Adding New Strategies
```python
# In strategy_engine.py
self.strategies["Your Strategy"] = {
    "description": "...",
    "philosophy": "...",
    "principles": [...],
    # ... other params
}
```

## 📁 File Structure

```
dk_pro_optimizer/
├── app.py                      # Streamlit UI
├── lineup_builder.py           # Core optimization logic
├── strategy_engine.py          # Strategy definitions
├── projection_analyzer.py      # Slate analysis tools
├── requirements.txt            # Dependencies
├── sample_nfl_projections.csv  # Example data
└── README.md                   # This file
```

## 🎓 Tips for Success

1. **Ownership is Everything**
   - Get accurate ownership projections (RotoGrinders, FantasyLabs)
   - Field is usually wrong on 3-5 players per slate
   - Find those players

2. **Don't Overthink Stacks**
   - QB + 1-2 pass catchers is enough
   - Bring-back from opposing team
   - Don't need to stack everything

3. **Value ≠ Good Play**
   - 6x value in a blowout = bad
   - Context matters more than raw value

4. **Test Your Strategy**
   - Track results over 20+ contests
   - Adjust based on what works
   - Every slate is different

5. **Avoid These Mistakes**
   - Being 100% contrarian (you're smarter than everyone!)
   - Chasing ownership without projection edge
   - Ignoring game theory
   - Over-optimizing (paralysis by analysis)

## 🔮 Future Enhancements

- Historical optimal lineup analysis
- Correlation matrix from actual game data
- Live ownership tracking
- Contest-specific optimization (Milly vs Sunday Million)
- Showdown slate optimizer
- Multi-slate tracking and ROI analysis

## 🙏 Credits

Built by someone who learned the hard way that being contrarian isn't the same as being smart.

Based on strategies from professional players like:
- Cal Spears (correlation theory)
- Saahil Sud (leverage concepts)
- Chris Raybon (ownership analysis)

## ⚖️ Disclaimer

This is a tool, not a guarantee. DFS involves risk and variance. The edge comes from:
1. Better projections than the field
2. Better ownership estimates than the field
3. Better game theory than the field

If you don't have at least one of these, you don't have an edge.

---

**Good luck, and remember: Don't be stupid contrarian. Be smart contrarian.**
