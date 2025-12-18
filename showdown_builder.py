import numpy as np
import pandas as pd
from typing import List, Dict

class ShowdownLineupBuilder:
    """
    Builds optimal DFS lineups for Showdown/Captain mode contests.
    Different optimization logic than classic tournaments.
    """
    
    def __init__(self, df: pd.DataFrame, sport: str, strategy: str,
                 ownership_weight: float, leverage_target: float, min_salary: int):
        
        self.df = df.copy()
        self.sport = sport
        self.strategy = strategy
        self.ownership_weight = ownership_weight
        self.leverage_target = leverage_target
        self.min_salary = min_salary
        
        # Showdown salary cap (typically 50K)
        self.salary_cap = 50000
        
        # Showdown roster: 1 CPT + 5 FLEX
        self.roster_size = 6
        
        self._preprocess_data()
    
    def _preprocess_data(self):
        """Prepare showdown data for optimization"""
        # CRITICAL FIX: Map column names FIRST
        column_mapping = {}
        for col in self.df.columns:
            col_clean = str(col).strip().replace('\xa0', ' ').replace('\u00a0', ' ').strip().lower()
            
            if col_clean in ['ownership', 'own', 'own%', 'own %', 'ownership%', 'ownership %']:
                column_mapping[col] = 'Ownership'
            elif col_clean in ['cpt ownership', 'cpt ownership%', 'cpt ownership %']:
                column_mapping[col] = 'CPT_Ownership'
            elif col_clean in ['cpt leverage']:
                column_mapping[col] = 'CPT_Leverage'
            elif col_clean in ['salary', 'sal', 'price']:
                column_mapping[col] = 'Salary'
            elif col_clean in ['projection', 'proj', 'fpts', 'points']:
                column_mapping[col] = 'Projection'
            elif col_clean in ['player', 'name']:
                column_mapping[col] = 'Name'
        
        if column_mapping:
            self.df.rename(columns=column_mapping, inplace=True)
        
        # Ensure we have CPT projections
        if 'CPT_Ownership' not in self.df.columns:
            # Create CPT versions if not provided
            self.df['CPT_Ownership'] = self.df['Ownership'] * 1.5  # CPT usually higher owned
        
        if 'CPT_Leverage' not in self.df.columns and 'CPT_Ownership' in self.df.columns:
            # Captain salary is 1.5x, projection is 1.5x
            cpt_projection = self.df['Projection'] * 1.5
            self.df['CPT_Leverage'] = cpt_projection / (self.df['CPT_Ownership'] + 0.1)
    
    def build_lineups(self, num_lineups: int) -> List[Dict]:
        """
        Build optimal showdown lineups.
        Returns list of lineup dictionaries with analytics.
        """
        lineups = []
        used_combinations = set()
        
        attempts = 0
        max_attempts = num_lineups * 2000
        
        while len(lineups) < num_lineups and attempts < max_attempts:
            attempts += 1
            
            lineup_players = self._build_single_lineup(used_combinations)
            
            if lineup_players:
                # Create combination signature
                sig = tuple(sorted([p['Name'] for p in lineup_players]))
                
                if sig not in used_combinations:
                    used_combinations.add(sig)
                    
                    # Calculate lineup metrics
                    lineup = self._create_lineup_dict(lineup_players)
                    lineups.append(lineup)
        
        # Sort by optimized score
        lineups.sort(key=lambda x: x['optimal_score'], reverse=True)
        
        return lineups
    
    def _build_single_lineup(self, used_combinations: set) -> List[Dict]:
        """Build a single showdown lineup"""
        lineup = []
        remaining_salary = self.salary_cap
        
        # 1. Select Captain (most critical decision in showdown)
        captain = self._select_captain()
        if captain is None:
            return None
        
        captain_dict = captain.to_dict()
        captain_dict['Role'] = 'CPT'
        captain_dict['Salary'] = int(captain['Salary'] * 1.5)  # Captain is 1.5x salary
        captain_dict['Projection'] = captain['Projection'] * 1.5  # Captain is 1.5x points
        captain_dict['Ownership'] = captain.get('CPT_Ownership', captain['Ownership'] * 1.5)
        captain_dict['Leverage'] = captain.get('CPT_Leverage', captain_dict['Projection'] / (captain_dict['Ownership'] + 0.1))
        
        lineup.append(captain_dict)
        remaining_salary -= captain_dict['Salary']
        
        # 2. Select 5 FLEX players
        flex_pool = self.df[
            (self.df['Name'] != captain['Name']) &
            (self.df['Salary'] <= remaining_salary)
        ].copy()
        
        if len(flex_pool) < 5:
            return None
        
        flex_players = self._select_flex_players(flex_pool, remaining_salary, 5)
        
        if len(flex_players) < 5:
            return None
        
        for player in flex_players:
            player_dict = player.to_dict()
            player_dict['Role'] = 'FLEX'
            lineup.append(player_dict)
            remaining_salary -= player['Salary']
        
        # Validate lineup
        total_salary = sum(p['Salary'] for p in lineup)
        if len(lineup) == 6 and total_salary <= self.salary_cap and total_salary >= self.min_salary:
            return lineup
        
        return None
    
    def _select_captain(self):
        """Select captain using strategy-specific logic"""
        captain_pool = self.df.copy()
        captain_pool['Random'] = np.random.random(len(captain_pool))
        
        if self.strategy == "Balanced GPP":
            # Mix of projection and CPT leverage
            cpt_lev = captain_pool.get('CPT_Leverage', captain_pool['Leverage'])
            captain_pool['Score'] = (
                captain_pool['Projection'] * 0.6 + 
                cpt_lev * 0.3 + 
                captain_pool['Random'] * 0.1
            )
        
        elif self.strategy == "Leverage Play":
            # Heavy CPT leverage emphasis
            cpt_lev = captain_pool.get('CPT_Leverage', captain_pool['Leverage'])
            captain_pool['Score'] = cpt_lev * 0.9 + captain_pool['Random'] * 0.1
        
        elif self.strategy == "Contrarian Core":
            # Low CPT ownership
            cpt_own = captain_pool.get('CPT_Ownership', captain_pool['Ownership'] * 1.5)
            captain_pool['Score'] = (
                captain_pool['Projection'] * 0.6 - 
                cpt_own * 0.3 + 
                captain_pool['Random'] * 0.1
            )
        
        elif self.strategy == "Ceiling Chaser":
            # Pure ceiling at captain
            captain_pool['Score'] = captain_pool['Ceiling'] * 0.8 + captain_pool['Random'] * 0.2
        
        else:
            # Default: projection-based
            captain_pool['Score'] = captain_pool['Projection'] * 0.7 + captain_pool['Random'] * 0.3
        
        # Select top scorer
        return captain_pool.nlargest(1, 'Score').iloc[0] if len(captain_pool) > 0 else None
    
    def _select_flex_players(self, pool: pd.DataFrame, remaining_salary: int, count: int):
        """Select FLEX players for showdown lineup"""
        pool = pool.copy()
        pool['Random'] = np.random.random(len(pool))
        
        # Strategy-specific scoring
        if self.strategy == "Balanced GPP":
            pool['Score'] = pool['Value'] * 0.5 + pool['Leverage'] * 0.4 + pool['Random'] * 0.1
        
        elif self.strategy == "Leverage Play":
            pool['Score'] = pool['Leverage'] * 0.8 + pool['Random'] * 0.2
        
        elif self.strategy == "Contrarian Core":
            pool['Score'] = pool['Projection'] * 0.6 - pool['Ownership'] * 0.3 + pool['Random'] * 0.1
        
        elif self.strategy == "Ceiling Chaser":
            pool['Score'] = pool['Ceiling'] * 0.7 + pool['Value'] * 0.3
        
        else:
            pool['Score'] = pool['Projection'] * 0.6 + pool['Value'] * 0.4
        
        # Iteratively select players
        selected = []
        for _ in range(count):
            if pool.empty:
                break
            
            # Filter by remaining salary
            affordable = pool[pool['Salary'] <= remaining_salary]
            if affordable.empty:
                break
            
            # Select best
            best = affordable.nlargest(1, 'Score').iloc[0]
            selected.append(best)
            
            # Update
            remaining_salary -= best['Salary']
            pool = pool[pool['Name'] != best['Name']]
        
        return selected
    
    def _create_lineup_dict(self, players: List[Dict]) -> Dict:
        """Create comprehensive lineup dictionary with analytics"""
        # Separate captain and flex
        captain = next(p for p in players if p['Role'] == 'CPT')
        flex = [p for p in players if p['Role'] == 'FLEX']
        
        total_salary = sum(p['Salary'] for p in players)
        total_proj = sum(p['Projection'] for p in players)
        avg_own = np.mean([p['Ownership'] for p in players])
        
        # Calculate leverage (weighted by salary/importance)
        captain_leverage = captain['Leverage'] * 1.5  # Captain is more important
        flex_leverage = sum(p['Leverage'] for p in flex)
        total_leverage = (captain_leverage + flex_leverage) / 6
        
        # Ceiling
        total_ceiling = sum(p.get('Ceiling', p['Projection'] * 1.3) for p in players)
        
        # Optimal score
        optimal_score = self._calculate_optimal_score(players)
        
        # Construction notes
        notes = self._generate_showdown_notes(players, captain)
        
        # Edge plays
        edges = self._identify_edge_plays(players)
        
        return {
            'players': players,
            'captain': captain['Name'],
            'salary': total_salary,
            'projection': total_proj,
            'avg_ownership': avg_own,
            'total_leverage': total_leverage,
            'ceiling': total_ceiling,
            'optimal_score': optimal_score,
            'stack_rating': self._rate_showdown_correlation(players),
            'construction_notes': notes,
            'edge_plays': edges
        }
    
    def _calculate_optimal_score(self, players: List[Dict]) -> float:
        """Calculate showdown-specific optimal score"""
        total_proj = sum(p['Projection'] for p in players)
        avg_own = np.mean([p['Ownership'] for p in players])
        
        # Captain leverage bonus
        captain = next(p for p in players if p['Role'] == 'CPT')
        captain_leverage_bonus = captain['Leverage'] * 2
        
        # Base score
        score = total_proj
        
        # Ownership adjustment
        ownership_penalty = (avg_own - 12) * self.ownership_weight * 0.5
        score = score - ownership_penalty + captain_leverage_bonus
        
        return score
    
    def _rate_showdown_correlation(self, players: List[Dict]) -> str:
        """Rate correlation in showdown lineup"""
        # In showdown, all players are from same game
        # Rate based on captain choice and flex correlation
        captain = next(p for p in players if p['Role'] == 'CPT')
        
        # Check if captain is a QB/star scorer
        if 'Position' in captain:
            if 'QB' in captain['Position'] or 'WR' in captain['Position']:
                return "Excellent"
        
        # Default rating based on leverage
        if captain['Leverage'] > 1.5:
            return "Good"
        elif captain['Leverage'] > 1.0:
            return "Fair"
        else:
            return "Poor"
    
    def _generate_showdown_notes(self, players: List[Dict], captain: Dict) -> List[str]:
        """Generate showdown-specific construction notes"""
        notes = []
        
        # Captain analysis
        captain_own = captain.get('Ownership', 0)
        if captain_own < 15:
            notes.append(f"Contrarian captain choice: {captain['Name']} at {captain_own:.1f}%")
        elif captain_own > 30:
            notes.append(f"Chalky captain: {captain['Name']} at {captain_own:.1f}%")
        else:
            notes.append(f"Balanced captain: {captain['Name']} at {captain_own:.1f}%")
        
        # Flex ownership distribution
        flex = [p for p in players if p['Role'] == 'FLEX']
        flex_own = [p['Ownership'] for p in flex]
        low_own_flex = sum(1 for o in flex_own if o < 10)
        
        if low_own_flex >= 3:
            notes.append(f"{low_own_flex} low-owned FLEX plays for differentiation")
        
        # Salary usage
        total_salary = sum(p['Salary'] for p in players)
        salary_pct = total_salary / self.salary_cap * 100
        notes.append(f"Using {salary_pct:.1f}% of salary cap")
        
        return notes
    
    def _identify_edge_plays(self, players: List[Dict]) -> List[str]:
        """Identify specific edges in showdown lineup"""
        edges = []
        
        captain = next(p for p in players if p['Role'] == 'CPT')
        if captain['Leverage'] > 1.5:
            edges.append(f"Captain {captain['Name']}: High leverage ({captain['Leverage']:.2f})")
        
        for p in players:
            if p['Role'] == 'FLEX':
                if p['Leverage'] > 1.5:
                    edges.append(f"{p['Name']}: High leverage ({p['Leverage']:.2f})")
                if p.get('Value', 0) > 1.0:
                    edges.append(f"{p['Name']}: Elite value ({p['Value']:.2f}x)")
        
        return edges[:5]
    
    def export_for_dk(self, lineups: List[Dict]) -> str:
        """Export lineups in DraftKings Showdown CSV format"""
        import io
        output = io.StringIO()
        
        # Showdown format: CPT, FLEX, FLEX, FLEX, FLEX, FLEX
        output.write("CPT,FLEX,FLEX,FLEX,FLEX,FLEX\n")
        
        for lineup in lineups:
            players = lineup['players']
            captain = next(p['Name'] for p in players if p['Role'] == 'CPT')
            flex = [p['Name'] for p in players if p['Role'] == 'FLEX']
            
            row = [captain] + flex
            output.write(','.join(row) + '\n')
        
        return output.getvalue()
