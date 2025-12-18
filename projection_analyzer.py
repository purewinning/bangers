# projection_analyzer.py - Version 1.3.2 - NUCLEAR FIX
# This version catches ANY 'Ownership' error and fixes it

import pandas as pd
import numpy as np
from typing import Dict, List

__version__ = "1.3.2"

class ProjectionAnalyzer:
    """
    Analyzes projection data to identify edges and opportunities.
    Version 1.3.2 - Nuclear fix for Ownership column
    """
    
    def __init__(self, df: pd.DataFrame, sport: str, contest_type: str = None):
        self.df = df.copy()
        self.sport = sport
        self.contest_type = contest_type
        
        # NUCLEAR FIX: Rename columns IMMEDIATELY before anything else
        self._fix_column_names_immediately()
        
        self._preprocess()
        self._detect_contest_type()
    
    def _fix_column_names_immediately(self):
        """
        NUCLEAR FIX: Rename columns RIGHT NOW before any other code runs
        This catches the error before it can happen
        """
        # Create a mapping of what we find → what we need
        new_columns = []
        
        for col in self.df.columns:
            col_str = str(col).strip().replace('\xa0', ' ').replace('\u00a0', ' ').strip()
            col_lower = col_str.lower()
            
            # Map to standard names IMMEDIATELY
            if col_lower in ['player', 'name', 'player name']:
                new_columns.append('Name')
            elif col_lower in ['salary', 'sal', 'price']:
                new_columns.append('Salary')
            elif col_lower in ['projection', 'proj', 'fpts', 'points']:
                new_columns.append('Projection')
            elif col_lower in ['ownership', 'own', 'own%', 'own %', 'ownership%', 'ownership %']:
                new_columns.append('Ownership')  # FIX IT NOW
            elif col_lower in ['position', 'pos']:
                new_columns.append('Position')
            elif col_lower in ['team', 'tm']:
                new_columns.append('Team')
            elif col_lower in ['opponent', 'opp']:
                new_columns.append('Opponent')
            elif col_lower in ['value', 'val']:
                new_columns.append('Value')
            elif col_lower in ['leverage', 'lev']:
                new_columns.append('Leverage')
            elif col_lower in ['optimal', 'optimal%', 'optimal %']:
                new_columns.append('Optimal')
            elif col_lower in ['std dev', 'stddev', 'std', 'stdev']:
                new_columns.append('StdDev')
            elif col_lower in ['cpt ownership', 'cpt ownership%', 'cpt ownership %', 'cpt own%']:
                new_columns.append('CPT_Ownership')
            elif col_lower in ['cpt optimal', 'cpt optimal%', 'cpt optimal %']:
                new_columns.append('CPT_Optimal')
            elif col_lower in ['cpt leverage']:
                new_columns.append('CPT_Leverage')
            else:
                # Keep original if not mapped
                new_columns.append(col_str)
        
        # Replace columns RIGHT NOW
        self.df.columns = new_columns
    
    def _preprocess(self):
        """Clean and prepare data - columns already fixed"""
        
        # Check for required columns (should already be renamed)
        required_cols = ['Salary', 'Projection', 'Ownership']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            available_cols = list(self.df.columns)
            raise ValueError(
                f"❌ Missing required columns: {', '.join(missing_cols)}\n\n"
                f"Available columns: {', '.join(available_cols)}\n\n"
                f"Version: {__version__}"
            )
        
        # Ensure Name column
        if 'Name' not in self.df.columns:
            if 'Player' in self.df.columns:
                self.df.rename(columns={'Player': 'Name'}, inplace=True)
            else:
                # Use first column as name
                self.df.rename(columns={self.df.columns[0]: 'Name'}, inplace=True)
        
        # Convert to numeric
        numeric_cols = ['Salary', 'Projection', 'Ownership']
        optional_numeric = ['Value', 'Leverage', 'Optimal', 'StdDev', 
                           'CPT_Ownership', 'CPT_Optimal', 'CPT_Leverage']
        
        for col in numeric_cols + optional_numeric:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove invalid rows
        self.df = self.df.dropna(subset=['Salary', 'Projection', 'Ownership'])
        
        # Calculate metrics
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
        """Detect contest type"""
        if self.contest_type:
            return
        
        has_cpt_columns = any('CPT' in str(col) for col in self.df.columns)
        
        if 'Position' in self.df.columns:
            has_cpt_position = self.df['Position'].str.contains('CPT|CAPTAIN', case=False, na=False).any()
        else:
            has_cpt_position = False
        
        self.contest_type = 'showdown' if (has_cpt_columns or has_cpt_position) else 'classic'
    
    def analyze(self) -> Dict:
        """Comprehensive slate analysis"""
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
        return len(self.df[self.df['Value'] > 1.0])
    
    def _count_leverage_plays(self) -> int:
        return len(self.df[self.df['Leverage'] > 1.5])
    
    def _identify_chalk(self) -> List[Dict]:
        chalk = self.df[self.df['Ownership'] > 25].copy()
        chalk = chalk.sort_values('Ownership', ascending=False).head(10)
        return chalk[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership']].to_dict('records')
    
    def _identify_leverage_opportunities(self) -> List[Dict]:
        leverage = self.df[
            (self.df['Leverage'] > 1.3) &
            (self.df['Projection'] > self.df['Projection'].quantile(0.6))
        ].copy()
        leverage = leverage.sort_values('Leverage', ascending=False).head(15)
        return leverage[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership', 'Leverage']].to_dict('records')
    
    def _identify_value_plays(self) -> List[Dict]:
        value = self.df[self.df['Value'] > 1.0].copy()
        value = value.sort_values('Value', ascending=False).head(15)
        return value[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership', 'Value']].to_dict('records')
    
    def _identify_contrarian_targets(self) -> List[Dict]:
        contrarian = self.df[
            (self.df['Ownership'] < 10) &
            (self.df['Projection'] > self.df['Projection'].quantile(0.5))
        ].copy()
        contrarian = contrarian.sort_values('Projection', ascending=False).head(15)
        return contrarian[['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership']].to_dict('records')
    
    def _analyze_salary_distribution(self) -> Dict:
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
        
        team_stacks = dict(sorted(team_stacks.items(), key=lambda x: x[1]['top_3_proj'], reverse=True))
        return team_stacks
