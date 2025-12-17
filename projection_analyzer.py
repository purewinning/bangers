import pandas as pd
import numpy as np
from typing import Dict, List

class ProjectionAnalyzer:
    """
    Analyzes projection data to identify edges and opportunities.
    Helps understand the slate dynamics before building lineups.
    """
    
    def __init__(self, df: pd.DataFrame, sport: str):
        self.df = df.copy()
        self.sport = sport
        self._preprocess()
    
    def _preprocess(self):
        """Clean and prepare data for analysis"""
        # Standardize columns
        self.df.columns = [col.strip() for col in self.df.columns]
        
        # Ensure numeric types
        numeric_cols = ['Salary', 'Projection', 'Ownership']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove invalid rows
        self.df = self.df.dropna(subset=['Salary', 'Projection', 'Ownership'])
        
        # Calculate metrics
        self.df['Value'] = self.df['Projection'] / (self.df['Salary'] / 1000)
        self.df['Leverage'] = self.df['Projection'] / (self.df['Ownership'] + 0.1)
        self.df['Ceiling'] = self.df['Projection'] * 1.3
    
    def analyze(self) -> Dict:
        """
        Comprehensive slate analysis.
        Returns key metrics and opportunities.
        """
        analysis = {
            'total_players': len(self.df),
            'avg_ownership': self.df['Ownership'].mean(),
            'median_ownership': self.df['Ownership'].median(),
            'value_count': self._count_value_plays(),
            'leverage_count': self._count_leverage_plays(),
            'chalk_plays': self._identify_chalk(),
            'leverage_opportunities': self._identify_leverage_opportunities(),
            'value_plays': self._identify_value_plays(),
            'contrarian_targets': self._identify_contrarian_targets(),
            'salary_distribution': self._analyze_salary_distribution(),
            'ownership_distribution': self._analyze_ownership_distribution()
        }
        
        if self.sport == "NFL":
            analysis['stacking_opportunities'] = self._analyze_nfl_stacks()
        else:
            analysis['team_stacks'] = self._analyze_nba_stacks()
        
        return analysis
    
    def _count_value_plays(self) -> int:
        """Count players with strong value (pts per $1K)"""
        return len(self.df[self.df['Value'] > 1.0])
    
    def _count_leverage_plays(self) -> int:
        """Count players with leverage > 1.5"""
        return len(self.df[self.df['Leverage'] > 1.5])
    
    def _identify_chalk(self) -> List[Dict]:
        """Identify chalk plays (>25% ownership)"""
        chalk = self.df[self.df['Ownership'] > 25].copy()
        chalk = chalk.sort_values('Ownership', ascending=False).head(10)
        
        return chalk[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership']].to_dict('records')
    
    def _identify_leverage_opportunities(self) -> List[Dict]:
        """Find best leverage plays"""
        # High projection, lower ownership
        leverage = self.df[
            (self.df['Leverage'] > 1.3) &
            (self.df['Projection'] > self.df['Projection'].quantile(0.6))
        ].copy()
        
        leverage = leverage.sort_values('Leverage', ascending=False).head(15)
        
        return leverage[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership', 'Leverage']].to_dict('records')
    
    def _identify_value_plays(self) -> List[Dict]:
        """Find best value plays"""
        value = self.df[self.df['Value'] > 1.0].copy()
        value = value.sort_values('Value', ascending=False).head(15)
        
        return value[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership', 'Value']].to_dict('records')
    
    def _identify_contrarian_targets(self) -> List[Dict]:
        """Find smart contrarian plays (low owned but with upside)"""
        # Low ownership but reasonable projection
        contrarian = self.df[
            (self.df['Ownership'] < 10) &
            (self.df['Projection'] > self.df['Projection'].quantile(0.5))
        ].copy()
        
        contrarian = contrarian.sort_values('Projection', ascending=False).head(15)
        
        return contrarian[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership']].to_dict('records')
    
    def _analyze_salary_distribution(self) -> Dict:
        """Analyze salary ranges by position"""
        distribution = {}
        
        if 'Position' in self.df.columns:
            for pos in self.df['Position'].unique():
                if pd.notna(pos):
                    pos_df = self.df[self.df['Position'].str.contains(pos, na=False)]
                    
                    if not pos_df.empty:
                        distribution[pos] = {
                            'min': int(pos_df['Salary'].min()),
                            'max': int(pos_df['Salary'].max()),
                            'median': int(pos_df['Salary'].median()),
                            'avg_proj': round(pos_df['Projection'].mean(), 2)
                        }
        
        return distribution
    
    def _analyze_ownership_distribution(self) -> Dict:
        """Analyze ownership distribution across the slate"""
        return {
            'chalk_count': len(self.df[self.df['Ownership'] > 25]),
            'medium_count': len(self.df[(self.df['Ownership'] >= 10) & (self.df['Ownership'] <= 25)]),
            'low_count': len(self.df[self.df['Ownership'] < 10]),
            'ownership_by_tier': {
                'Elite (>30%)': len(self.df[self.df['Ownership'] > 30]),
                'High (20-30%)': len(self.df[(self.df['Ownership'] >= 20) & (self.df['Ownership'] < 30)]),
                'Medium (10-20%)': len(self.df[(self.df['Ownership'] >= 10) & (self.df['Ownership'] < 20)]),
                'Low (5-10%)': len(self.df[(self.df['Ownership'] >= 5) & (self.df['Ownership'] < 10)]),
                'Very Low (<5%)': len(self.df[self.df['Ownership'] < 5])
            }
        }
    
    def _analyze_nfl_stacks(self) -> Dict:
        """Analyze NFL stacking opportunities"""
        stacks = {}
        
        if 'Game' not in self.df.columns:
            return {"message": "Game information not available for stack analysis"}
        
        # Group by game
        games = self.df['Game'].dropna().unique()
        
        for game in games:
            game_players = self.df[self.df['Game'] == game]
            
            # Find QBs in the game
            qbs = game_players[game_players['Position'].str.contains('QB', na=False)]
            
            for _, qb in qbs.iterrows():
                qb_team = qb['Team']
                
                # Find pass catchers on same team
                pass_catchers = game_players[
                    (game_players['Team'] == qb_team) &
                    (game_players['Position'].str.contains('WR|TE', na=False))
                ]
                
                if not pass_catchers.empty:
                    stack_proj = qb['Projection'] + pass_catchers.nlargest(2, 'Projection')['Projection'].sum()
                    stack_own = (qb['Ownership'] + pass_catchers.nlargest(2, 'Projection')['Ownership'].sum()) / 3
                    
                    stacks[f"{qb['Name']} Stack"] = {
                        'qb': qb['Name'],
                        'qb_own': round(qb['Ownership'], 1),
                        'top_catchers': pass_catchers.nlargest(3, 'Projection')[['Name', 'Position', 'Ownership']].to_dict('records'),
                        'stack_projection': round(stack_proj, 2),
                        'stack_ownership': round(stack_own, 1),
                        'game': game
                    }
        
        return stacks
    
    def _analyze_nba_stacks(self) -> Dict:
        """Analyze NBA team stacking opportunities"""
        if 'Team' not in self.df.columns:
            return {"message": "Team information not available"}
        
        team_stacks = {}
        
        for team in self.df['Team'].unique():
            if pd.notna(team):
                team_players = self.df[self.df['Team'] == team]
                
                # Top 3 projected players from team
                top_players = team_players.nlargest(3, 'Projection')
                
                team_stacks[team] = {
                    'total_players': len(team_players),
                    'avg_projection': round(team_players['Projection'].mean(), 2),
                    'avg_ownership': round(team_players['Ownership'].mean(), 1),
                    'top_3_proj': round(top_players['Projection'].sum(), 2),
                    'top_players': top_players[['Name', 'Position', 'Projection', 'Ownership']].to_dict('records')
                }
        
        # Sort by top 3 projection
        team_stacks = dict(sorted(team_stacks.items(), 
                                  key=lambda x: x[1]['top_3_proj'], 
                                  reverse=True))
        
        return team_stacks
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        Build correlation matrix for players.
        In production, this would use historical data.
        """
        # Simplified placeholder
        if self.sport == "NFL":
            return self._nfl_correlation_matrix()
        else:
            return self._nba_correlation_matrix()
    
    def _nfl_correlation_matrix(self) -> pd.DataFrame:
        """NFL position correlations"""
        # These are theoretical correlations
        correlations = {
            'QB-WR (same team)': 0.65,
            'QB-TE (same team)': 0.55,
            'QB-RB (same team)': -0.15,
            'RB-DST (same team)': -0.30,
            'WR-WR (same team)': -0.10,
            'Opposing skill positions': 0.20
        }
        
        return pd.DataFrame(list(correlations.items()), 
                          columns=['Relationship', 'Correlation'])
    
    def _nba_correlation_matrix(self) -> pd.DataFrame:
        """NBA position correlations"""
        correlations = {
            'Teammates (general)': 0.15,
            'PG-SG (same team)': 0.25,
            'Opposing stars': 0.30,
            'Blowout scenarios': -0.40
        }
        
        return pd.DataFrame(list(correlations.items()),
                          columns=['Relationship', 'Correlation'])
    
    def generate_slate_report(self) -> str:
        """Generate a text report of slate analysis"""
        analysis = self.analyze()
        
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    SLATE ANALYSIS REPORT                       ║
╚═══════════════════════════════════════════════════════════════╝

OVERVIEW
--------
Total Players: {analysis['total_players']}
Average Ownership: {analysis['avg_ownership']:.1f}%
Value Plays Available: {analysis['value_count']}
Leverage Opportunities: {analysis['leverage_count']}

CHALK PLAYS (>25% Ownership)
-----------------------------
"""
        
        for player in analysis['chalk_plays'][:5]:
            report += f"  • {player['Name']} ({player['Position']}) - {player['Ownership']:.1f}% @ ${player['Salary']:,}\n"
        
        report += f"""
LEVERAGE OPPORTUNITIES
----------------------
"""
        
        for player in analysis['leverage_opportunities'][:5]:
            report += f"  • {player['Name']} - Proj: {player['Projection']:.1f} / Own: {player['Ownership']:.1f}% (Leverage: {player['Leverage']:.2f})\n"
        
        report += f"""
OWNERSHIP DISTRIBUTION
---------------------
Chalk (>25%): {analysis['ownership_distribution']['chalk_count']} players
Medium (10-25%): {analysis['ownership_distribution']['medium_count']} players
Low (<10%): {analysis['ownership_distribution']['low_count']} players

STRATEGY RECOMMENDATIONS
-----------------------
"""
        
        if analysis['avg_ownership'] > 15:
            report += "  ⚠️  High average ownership - consider contrarian core strategy\n"
        if analysis['leverage_count'] > 20:
            report += "  ✓  Multiple leverage opportunities - leverage play strategy recommended\n"
        if len(analysis['chalk_plays']) > 10:
            report += "  ⚠️  Chalky slate - differentiation will be key\n"
        
        return report
