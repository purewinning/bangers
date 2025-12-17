# DK Pro Optimizer - Quick Start Guide

## Getting Your Projections Ready

### Required CSV Format
Your CSV needs these columns:
- **Name**: Player name
- **Position**: QB, RB, WR, TE, DST (NFL) or PG, SG, SF, PF, C (NBA)
- **Team**: 3-letter team abbreviation
- **Salary**: DraftKings salary (e.g., 8500)
- **Projection**: Your fantasy point projection
- **Ownership**: Projected ownership percentage (e.g., 15.5 for 15.5%)

### Optional but Recommended (NFL)
- **Game**: Game info like "KC@BUF" for correlation analysis

### Where to Get Ownership Projections
- RotoGrinders (paid)
- FantasyLabs (paid)
- DailyRoto (paid)
- Your own model
- DraftKings' own projections (less accurate)

## Running the App

### Option 1: Using the Script
```bash
./run.sh
```

### Option 2: Direct Command
```bash
streamlit run app.py
```

The app opens at: http://localhost:8501

## Strategy Selection Guide

### Contest Size < 10K Entries
**Recommended:** Balanced GPP
- You can win with good chalk plays
- Focus on value and leverage balance

### Contest Size 10K-50K Entries
**Recommended:** Leverage Play
- Need differentiation but not stupid contrarian
- Exploit ownership inefficiencies

### Contest Size 50K-150K Entries
**Recommended:** Contrarian Core or Balanced GPP
- More differentiation needed
- 3-5 low-owned pieces with upside

### Contest Size 150K+ Entries (Milly Maker)
**Recommended:** Ceiling Chaser or Contrarian Core
- Need tournament-winning ceiling
- Min-cash doesn't matter

### High Buy-In ($100+) Single Entry
**Recommended:** Leverage Play or Balanced GPP
- Professionals in these contests
- Edge comes from better ownership reads
- Avoid being too tricky

## Parameter Settings

### For Beginners
- Ownership Weight: 0.7
- Correlation Focus: 0.5
- Leverage Target: 1.0
- Min Salary: 48000

### For Advanced Players
- Ownership Weight: 0.8-0.9 (more ownership-conscious)
- Correlation Focus: 0.6-0.8 (stronger stacks)
- Leverage Target: 1.1-1.2 (seeking leverage)
- Min Salary: 49000 (using full cap)

## Understanding Your Lineups

### Good Single-Entry Lineup Characteristics
- **Total Leverage:** 1.0-1.2
- **Avg Ownership:** 10-15%
- **Stack Rating:** Good or Excellent
- **Edge Plays:** 3-5 identified edges
- **Salary Used:** 97-99% of cap

### Red Flags
- Total Leverage < 0.8 (too chalky)
- Avg Ownership > 20% (no differentiation)
- Salary Used < 95% (leaving value on table)
- No correlation/stacking
- All low-owned players (stupid contrarian)

## NFL-Specific Tips

### Stack Properly
✅ QB + 1-2 pass catchers from same team
✅ Bring-back from opposing team
✅ Primary stack from 2nd-highest total game

❌ QB + RB + WR from same team (over-correlated)
❌ RB + DST from same team (negative correlation)
❌ Stacking lowest-total game

### Position Strategy
- **QB:** Best leverage spot. Mid-tier in good matchup > expensive in bad matchup
- **RB:** Touch volume is king. Game script matters.
- **WR:** Target slot receivers and true WR1s. Avoid WR2/3 on run-heavy teams.
- **TE:** Chalk the elite ones or punt. Middle-tier TEs are traps.
- **DST:** Stream matchups. Don't overthink it.

## NBA-Specific Tips

### Stacking
- 2-3 players from high-pace teams
- Target teams with injury news (increased usage)
- Opposing stars in shootout games

### Position Strategy
- **PG/SG:** Usage rate and minutes most important
- **SF/PF:** Target forwards against bad defenses
- **C:** Big men against teams that allow paint points
- **UTIL:** Use for best remaining value

## Common Mistakes to Avoid

### 1. Being 100% Contrarian
❌ All players under 10% ownership
✅ 3-5 low-owned pieces, rest normal

### 2. Chasing Ownership Without Edge
❌ Fading 35% owned player just because
✅ Fading when you have a legitimate better option

### 3. Ignoring Correlation
❌ No stacking or game correlation
✅ Proper QB stack with bring-back

### 4. Poor Leverage Spots
❌ Spending up at DST for differentiation
✅ Differentiating at QB, RB, or WR

### 5. Leaving Money on Table
❌ $47,500 salary used
✅ $49,000+ salary used

## Exporting Lineups

1. Generate your optimal lineups
2. Review analytics and edge plays
3. Select "DraftKings CSV" export format
4. Download the CSV
5. Upload directly to DraftKings

The CSV is properly formatted for DK upload.

## Tracking Your Results

Keep a simple spreadsheet:
- Contest name
- Buy-in
- Strategy used
- Lineup ownership
- Finish position
- Profit/Loss

After 20+ contests, analyze:
- Which strategies work best for you
- Which slates you perform well on
- ROI by contest size

## Getting Better

### Learn From Winners
Study winning lineups:
- Where did they differentiate?
- What stacks did they use?
- What was their ownership profile?

### Improve Your Projections
Better projections = bigger edge
- Build your own models
- Adjust expert projections
- Factor in your own research

### Master Ownership Projection
This is the real edge:
- Field overreacts to news
- Field underweights certain game scripts
- Field follows "expert" chalk

## Support & Questions

For questions or issues:
1. Check the main README.md
2. Review strategy descriptions in app
3. Test with sample_nfl_projections.csv first

---

**Remember: This is a tool. Your edge comes from better information (projections, ownership, game theory) than the field.**

Good luck, and don't be stupid contrarian!
