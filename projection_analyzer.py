# projection_analyzer.py - Version 1.3.1 - STREAMLIT CLOUD FIX
# Force reload by changing version number

import pandas as pd
import numpy as np
from typing import Dict, List

# VERSION STAMP - increment this to force reload on Streamlit Cloud
__version__ = "1.3.1"

class ProjectionAnalyzer:
    """
    Analyzes projection data to identify edges and opportunities.
    Helps understand the slate dynamics before building lineups.
    
    Version 1.3.1 - Ownership column fix for Streamlit Cloud
    """
    
    def __init__(self, df: pd.DataFrame, sport: str, contest_type: str = None):
        self.df = df.copy()
        self.sport = sport
        self.contest_type = contest_type  # 'classic' or 'showdown'
        self._preprocess()
        self._detect_contest_type()
    
    def _preprocess(self):
        """Clean and prepare data for analysis - FIXED for 'Ownership %' """
        
        # STREAMLIT CLOUD FIX: Aggressive column cleaning
        # Strip ALL whitespace variations, unicode chars, and special chars
        self.df.columns = [
            str(col).strip()
                    .replace('\xa0', ' ')      # Non-breaking space
                    .replace('\u00a0', ' ')    # Unicode non-breaking space  
                    .replace('\u202f', ' ')    # Narrow non-breaking space
                    .replace('\t', ' ')         # Tabs
                    .strip()                    # Strip again after replacements
            for col in self.df.columns
        ]
        
        # CRITICAL FIX: Map columns using if/elif chain instead of dict
        # This catches "Ownership %" with the space!
        column_mapping = {}
        
        for col in self.df.columns:
            col_clean = col.lower().strip()
            
            # Name mappings
            if col_clean in ['player', 'name', 'player name', 'playername']:
                column_mapping[col] = 'Name'
            
            # Salary mappings
            elif col_clean in ['salary', 'sal', 'price']:
                column_mapping[col] = 'Salary'
            
            # Projection mappings
            elif col_clean in ['projection', 'proj', 'fpts', 'points', 'avgpoints', 'avg points']:
                column_mapping[col] = 'Projection'
            
            # OWNERSHIP MAPPINGS - THE CRITICAL FIX
            elif col_clean in ['ownership', 'own', 'own%', 'own %', 'ownership%', 'ownership %', 'ownership  %', 'projected ownership', 'proj own']:
                column_mapping[col] = 'Ownership'
            
            # Position
            elif col_clean in ['position', 'pos']:
                column_mapping[col] = 'Position'
            
            # Team
            elif col_clean in ['team', 'tm']:
                column_mapping[col] = 'Team'
            
            # Opponent
            elif col_clean in ['opponent', 'opp']:
                column_mapping[col] = 'Opponent'
            
            # Value
            elif col_clean in ['value', 'val']:
                column_mapping[col] = 'Value'
            
            # Leverage
            elif col_clean in ['leverage', 'lev']:
                column_mapping[col] = 'Leverage'
            
            # Optimal
            elif col_clean in ['optimal', 'optimal%', 'optimal %', 'optimal  %']:
                column_mapping[col] = 'Optimal'
            
            # Std Dev
            elif col_clean in ['std dev', 'stddev', 'std', 'stdev', 'sd']:
                column_mapping[col] = 'StdDev'
            
            # CPT columns (showdown)
            elif col_clean in ['cpt ownership', 'cpt ownership%', 'cpt ownership %', 'cpt own', 'cpt own%']:
                column_mapping[col] = 'CPT_Ownership'
            elif col_clean in ['cpt optimal', 'cpt optimal%', 'cpt optimal %']:
                column_mapping[col] = 'CPT_Optimal'
            elif col_clean in ['cpt leverage']:
                column_mapping[col] = 'CPT_Leverage'
        
        # Apply the mapping
        if column_mapping:
            self.df.rename(columns=column_mapping, inplace=True)
        
        # Check for required columns
        required_cols = ['Salary', 'Projection', 'Ownership']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        # If still missing, show helpful error
        if missing_cols:
            available_cols = list(self.df.columns)
            
            error_msg = (
                f"❌ Missing required columns: {', '.join(missing_cols)}\n\n"
                f"Your CSV must include:\n"
                f"  • Salary (or 'Price', 'Sal')\n"
                f"  • Projection (or 'Proj', 'FPTS', 'Points')\n"
                f"  • Ownership (or 'Own', 'Own %', 'Ownership %')\n\n"
                f"📋 Columns found in your file:\n"
            )
            
            for i, col in enumerate(available_cols[:15], 1):
                error_msg += f"  {i}. '{col}'\n"
            
            if len(available_cols) > 15:
                error_msg += f"  ... and {len(available_cols) - 15} more\n"
            
            error_msg += f"\n💡 Version: {__version__}"
            
            raise ValueError(error_msg)
        
        # Ensure Name column exists
        if 'Name' not in self.df.columns:
            if 'Player' in self.df.columns:
                self.df.rename(columns={'Player': 'Name'}, inplace=True)
            else:
                raise ValueError("❌ Missing 'Name' or 'Player' column")
        
        # Ensure numeric types
        numeric_cols = ['Salary', 'Projection', 'Ownership']
        optional_numeric = ['Value', 'Leverage', 'Optimal', 'StdDev', 
                           'CPT_Ownership', 'CPT_Optimal', 'CPT_Leverage']
        
        for col in numeric_cols + optional_numeric:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove invalid rows
        self.df = self.df.dropna(subset=['Salary', 'Projection', 'Ownership'])
        
        # Calculate metrics if not provided
        if 'Value' not in self.df.columns or self.df['Value'].isna().all():
            self.df['Value'] = self.df['Projection'] / (self.df['Salary'] / 1000)
        
        if 'Leverage' not in self.df.columns or self.df['Leverage'].isna().all():
            self.df['Leverage'] = self.df['Projection'] / (self.df['Ownership'] + 0.1)
        
        if 'Ceiling' not in self.df.columns or self.df['Ceiling'].isna().all():
            if 'StdDev' in self.df.columns and not self.df['StdDev'].isna().all():
                self.df['Ceiling'] = self.df['Projection'] + (1.5 * self.df['StdDev'])
            else:
                self.df['Ceiling'] = self.df['Projection'] * 1.3
    
    def _detect_contest_type(self):
        """Detect if this is a showdown or classic contest"""
        if self.contest_type:
            return  # Already set
        
        # Check for CPT columns
        has_cpt_columns = any('CPT' in str(col) for col in self.df.columns)
        
        # Check for captain positions
        if 'Position' in self.df.columns:
            has_cpt_position = self.df['Position'].str.contains('CPT|CAPTAIN', case=False, na=False).any()
        else:
            has_cpt_position = False
        
        if has_cpt_columns or has_cpt_position:
            self.contest_type = 'showdown'
        else:
            self.contest_type = 'classic'
    
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
        """Find smart contrarian plays"""
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
                    pos_df = self.df[self.df['Position'].str.contains(str(pos), na=False)]
                    
                    if not pos_df.empty:
                        distribution[pos] = {
                            'min': int(pos_df['Salary'].min()),
                            'max': int(pos_df['Salary'].max()),
                            'median': int(pos_df['Salary'].median()),
                            'avg_proj': round(pos_df['Projection'].mean(), 2)
                        }
        
        return distribution
    
    def _analyze_ownership_distribution(self) -> Dict:
        """Analyze ownership distribution"""
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
            return {"message": "Game information not available"}
        
        games = self.df['Game'].dropna().unique()
        
        for game in games:
            game_players = self.df[self.df['Game'] == game]
            qbs = game_players[game_players['Position'].str.contains('QB', na=False)]
            
            for _, qb in qbs.iterrows():
                qb_team = qb['Team']
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
        """Analyze NBA team stacking"""
        if 'Team' not in self.df.columns:
            return {"message": "Team information not available"}
        
        team_stacks = {}
        
        for team in self.df['Team'].unique():
            if pd.notna(team):
                team_players = self.df[self.df['Team'] == team]
                top_players = team_players.nlargest(3, 'Projection')
                
                team_stacks[team] = {
                    'total_players': len(team_players),
                    'avg_projection': round(team_players['Projection'].mean(), 2),
                    'avg_ownership': round(team_players['Ownership'].mean(), 1),
                    'top_3_proj': round(top_players['Projection'].sum(), 2),
                    'top_players': top_players[['Name', 'Position', 'Projection', 'Ownership']].to_dict('records')
                }
        
        team_stacks = dict(sorted(team_stacks.items(), 
                                  key=lambda x: x[1]['top_3_proj'], 
                                  reverse=True))
        
        return team_stacks
