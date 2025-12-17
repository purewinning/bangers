# Showdown Mode & Enhanced CSV Support - v1.2

## New Features

### 🎯 Showdown/Captain Mode Support

The optimizer now fully supports DraftKings Showdown contests where:
- You select 1 **Captain** (1.5x points, 1.5x salary)
- Plus 5 **FLEX** players
- All players from the same game

**Showdown-Specific Strategies:**
- Captain leverage is weighted more heavily
- Different ownership dynamics (CPT ownership vs FLEX ownership)
- Single-game correlation automatically handled
- Optimal captain selection based on leverage ratios

### 📊 Enhanced CSV Format Support

The optimizer now recognizes **all these column variations**:

| Standard | Accepted Variations |
|----------|-------------------|
| **Name** | Player, Player Name |
| **Salary** | Price, Sal |
| **Projection** | Proj, FPTS, Points |
| **Ownership** | Own, Own%, Ownership %, Ownership % |
| **Position** | Pos |
| **Team** | Tm |
| **Opponent** | Opp |
| **Value** | Val *(auto-calculated if missing)* |
| **Leverage** | Lev *(auto-calculated if missing)* |
| **Optimal** | Optimal%, Optimal % |
| **Std Dev** | StdDev, Std, StDev |

### 🆕 Captain-Specific Columns

For Showdown contests, these columns are recognized:

| Column | Purpose |
|--------|---------|
| **CPT Ownership %** | Projected ownership when played as captain |
| **CPT Optimal %** | Optimal ownership percentage for captain |
| **CPT Leverage** | Leverage ratio when played as captain |

*If CPT columns are missing, the optimizer will calculate them automatically.*

## Supported CSV Formats

### Classic Format (Original)
```csv
Name,Position,Team,Salary,Projection,Ownership
Patrick Mahomes,QB,KC,8500,24.5,28.5
Travis Kelce,TE,KC,7500,17.2,32.4
```

### Enhanced Format (Your Format)
```csv
Player,Salary,Position,Team,Opponent,Projection,Value,Ownership %,Optimal %,Leverage,CPT Ownership %,CPT Optimal %,CPT Leverage,Std Dev
Patrick Mahomes,11400,QB,KC,BUF,23.5,2.06,32.5,28.3,0.72,45.2,38.1,0.78,6.2
Travis Kelce,9800,TE,KC,BUF,16.2,1.65,28.3,24.7,0.57,38.7,32.4,0.63,4.8
```

**Both formats work perfectly!**

## Using Showdown Mode

### Automatic Detection
The optimizer automatically detects showdown contests by looking for:
- CPT-specific columns (CPT Ownership %, etc.)
- Captain positions in the data
- Roster structure

### Manual Selection
You can also manually select "Showdown" from the Contest Type dropdown in the sidebar.

### Showdown Lineup Display
Showdown lineups show:
- **Captain** highlighted in the lineup title
- **Role** column (CPT or FLEX)
- Captain-adjusted projections and ownership
- Showdown-specific construction notes

## Strategy Adjustments for Showdown

### Balanced GPP (Showdown)
- Mix of chalky and leverage captain choices
- 2-3 low-owned FLEX plays
- Captain leverage weighted heavily

### Leverage Play (Showdown)
- Captain with highest CPT leverage ratio
- 3-4 medium-owned FLEX
- Emphasis on captain differentiation

### Contrarian Core (Showdown)
- Low-owned captain (<15%)
- 3+ low-owned FLEX players
- Maximum differentiation strategy

### Ceiling Chaser (Showdown)
- Highest ceiling captain
- Boom/bust FLEX plays
- Pure upside optimization

## Example: Showdown Lineup

```
🏆 Lineup 1 - Projection: 78.2 | Salary: $49,800 | Ownership: 14.2% | Captain: Josh Allen

Player              Role  Position  Team  Salary  Projection  Ownership  Leverage
Josh Allen          CPT   QB        BUF   $16,800  34.2       48.5%      0.71
Travis Kelce        FLEX  TE        KC    $9,800   16.2       28.3%      0.57
Rashee Rice         FLEX  WR        KC    $6,400   10.2       8.5%       1.20
James Cook          FLEX  RB        BUF   $7,600   12.8       15.2%      0.84
Khalil Shakir       FLEX  WR        BUF   $5,800   9.1        6.8%       1.34
Noah Gray           FLEX  TE        KC    $5,200   7.8        5.2%       1.50

Total Leverage: 1.18
Ceiling Score: 92.4
Stack Rating: Excellent

Build Notes:
- Balanced captain: Josh Allen at 48.5%
- 3 low-owned FLEX plays for differentiation
- Using 99.6% of salary cap

Edge Plays:
- Noah Gray: High leverage (1.50)
- Khalil Shakir: High leverage (1.34)
- Rashee Rice: High leverage (1.20)
```

## Key Differences: Showdown vs Classic

| Aspect | Classic | Showdown |
|--------|---------|----------|
| **Roster** | 9 players, specific positions | 6 players (1 CPT + 5 FLEX) |
| **Salary Cap** | $50,000 | $50,000 |
| **Captain** | None | 1.5x points & salary |
| **Game Stack** | Optional correlation | All same game |
| **Positions** | QB/RB/WR/TE/DST/FLEX | Any position eligible |
| **Strategy Focus** | Multi-game stacking | Captain selection |

## Tips for Showdown Success

### Captain Selection
✅ **DO:**
- Captain with high leverage (low CPT own, high projection)
- Consider game script (who will dominate?)
- Use contrarian captains in large fields

❌ **DON'T:**
- Auto-captain the highest projected player
- Ignore CPT ownership vs FLEX ownership
- Forget captain is 1.5x salary

### FLEX Construction
✅ **DO:**
- Mix chalk and leverage FLEX
- 2-3 low-owned plays for differentiation
- Consider bring-backs (both teams)

❌ **DON'T:**
- Go all cheap to afford expensive captain
- Use all players from one team
- Ignore salary efficiency

### Contest-Specific Strategy

**Small Showdowns (<5K entries):**
- Balanced captain choices work
- 1-2 leverage FLEX plays
- Can win with some chalk

**Large Showdowns (20K+ entries):**
- Need captain differentiation
- 3-4 low-owned FLEX
- Higher variance required

## CSV Column Priority

If your CSV has both Value and can calculate value from Projection/Salary:
- **The optimizer uses your provided Value** (respects your calculations)

If missing, it calculates:
```
Value = Projection / (Salary / 1000)
Leverage = Projection / (Ownership + 0.1)
Ceiling = Projection + (1.5 × Std Dev)  [if Std Dev provided]
Ceiling = Projection × 1.3  [if no Std Dev]
```

## Testing the New Features

### Test Classic Mode
Upload: `sample_nfl_projections.csv`

### Test Showdown Mode
Upload: `sample_showdown_projections.csv`

Both files are included in the optimizer package!

## Troubleshooting

### "Missing required columns" Error
- Check that you have: Player/Name, Salary, Projection, Ownership %
- Column names are case-insensitive
- Variations like "Own%" are automatically recognized

### Showdown Not Detected
- Make sure Contest Type is set to "Showdown" in sidebar
- Or include CPT columns in your CSV for auto-detection

### Captain Not Showing
- Check that CPT Ownership % column exists
- Or let optimizer calculate it automatically (1.5x FLEX ownership)

## What's Auto-Calculated

Even if your CSV is missing these columns, the optimizer calculates:

✅ **Value** - from Projection and Salary
✅ **Leverage** - from Projection and Ownership
✅ **Ceiling** - from Projection (and Std Dev if available)
✅ **CPT_Ownership** - 1.5x FLEX ownership
✅ **CPT_Leverage** - from CPT projection and CPT ownership

**You only NEED: Player, Salary, Projection, Ownership %**

Everything else is optional or calculated!

---

## Quick Start: Showdown Example

1. **Load sample showdown CSV**
   ```
   Upload: sample_showdown_projections.csv
   ```

2. **Select settings**
   ```
   Sport: NFL
   Contest Type: Showdown (auto-detects)
   Strategy: Leverage Play
   ```

3. **Generate lineups**
   ```
   Click: 🚀 Generate Optimal Lineups
   ```

4. **Review captain choice**
   ```
   Check: Captain leverage and ownership
   Analyze: FLEX differentiation
   ```

5. **Export for DK**
   ```
   Format: CPT, FLEX, FLEX, FLEX, FLEX, FLEX
   ```

**That's it! Showdown optimization made easy.** 🎯
