import numpy as np
import pandas as pd
from itertools import combinations, product
from typing import List, Dict, Tuple
import random

class LineupBuilder:
    """
    Builds optimal DFS lineups using professional tournament strategies.
    Focuses on leverage, correlation, and ownership patterns that win tournaments.
    """
    
    def __init__(self, df: pd.DataFrame, sport: str, strategy: str,
                 ownership_weight: float, correlation_focus: float, 
                 leverage_target: float, min_salary: int):
        
        self.df = df.copy()
        self.sport = sport
        self.strategy = strategy
        self.ownership_weight = ownership_weight
        self.correlation_focus = correlation_focus
        self.leverage_target = leverage_target
        self.min_salary = min_salary
        
        # Salary cap
        self.salary_cap = 50000
        
        # Position requirements
        if sport == "NFL":
            self.positions = {
                'QB': 1, 'RB': 2, 'WR': 3, 'TE': 1, 'FLEX': 1, 'DST': 1
            }
        else:  # NBA
            self.positions = {
                'PG': 1, 'SG': 1, 'SF': 1, 'PF': 1, 'C': 1, 'G': 1, 'F': 1, 'UTIL': 1
            }
        
        self._preprocess_data()
        self._calculate_metrics()
    
    def _preprocess_data(self):
        """Clean and prepare data for optimization"""
        # CRITICAL FIX: Map column names FIRST before accessing them
        column_mapping = {}
        for col in self.df.columns:
            col_clean = str(col).strip().replace('\xa0', ' ').replace('\u00a0', ' ').strip().lower()
            
            if col_clean in ['ownership', 'own', 'own%', 'own %', 'ownership%', 'ownership %']:
                column_mapping[col] = 'Ownership'
            elif col_clean in ['salary', 'sal', 'price']:
                column_mapping[col] = 'Salary'
            elif col_clean in ['projection', 'proj', 'fpts', 'points']:
                column_mapping[col] = 'Projection'
            elif col_clean in ['player', 'name']:
                column_mapping[col] = 'Name'
            elif col_clean in ['position', 'pos']:
                column_mapping[col] = 'Position'
            elif col_clean in ['team', 'tm']:
                column_mapping[col] = 'Team'
        
        if column_mapping:
            self.df.rename(columns=column_mapping, inplace=True)
        
        # Ensure numeric types
        self.df['Salary'] = pd.to_numeric(self.df['Salary'], errors='coerce')
        self.df['Projection'] = pd.to_numeric(self.df['Projection'], errors='coerce')
        self.df['Ownership'] = pd.to_numeric(self.df['Ownership'], errors='coerce')
        
        # Remove invalid rows
        self.df = self.df.dropna(subset=['Salary', 'Projection', 'Ownership'])
        self.df = self.df[self.df['Projection'] > 0]
        
        # Handle multi-position players
        self.df['Positions'] = self.df['Position'].str.split('/')
    
    def _calculate_metrics(self):
        """Calculate advanced metrics for optimization"""
        # Base value
        self.df['Value'] = self.df['Projection'] / (self.df['Salary'] / 1000)
        
        # Leverage (projection to ownership ratio)
        self.df['Leverage'] = self.df['Projection'] / (self.df['Ownership'] + 0.1)
        
        # Ceiling (upside potential)
        self.df['Ceiling'] = self.df['Projection'] * 1.3  # Simplified ceiling
        
        # Ownership tier classification
        self.df['Own_Tier'] = pd.cut(
            self.df['Ownership'],
            bins=[0, 5, 15, 30, 100],
            labels=['Low', 'Medium', 'High', 'Chalk']
        )
        
        # Volatility score (for tournament upside)
        self.df['Volatility'] = np.random.normal(1.0, 0.15, len(self.df))  # Placeholder
        
    def _calculate_optimal_score(self, players: List[Dict]) -> float:
        """
        Calculate optimized score based on strategy.
        This is the secret sauce - weighing projection, ownership, and leverage.
        """
        total_proj = sum(p['Projection'] for p in players)
        avg_own = np.mean([p['Ownership'] for p in players])
        total_leverage = sum(p['Leverage'] for p in players)
        
        # Base score is projection
        score = total_proj
        
        # Strategy-specific adjustments
        if self.strategy == "Balanced GPP":
            # Reward moderate ownership and good leverage
            ownership_penalty = (avg_own - 10) * self.ownership_weight * 0.5
            leverage_bonus = (total_leverage / len(players)) * 2
            score = score - ownership_penalty + leverage_bonus
            
        elif self.strategy == "Leverage Play":
            # Heavy emphasis on leverage ratio
            leverage_ratio = total_leverage / len(players)
            leverage_bonus = (leverage_ratio - self.leverage_target) * 10
            score = score + leverage_bonus
            
        elif self.strategy == "Contrarian Core":
            # Reward low ownership core, but not stupidly
            # We want 3-4 players under 10% ownership, rest can be normal
            low_own_count = sum(1 for p in players if p['Ownership'] < 10)
            if 3 <= low_own_count <= 5:
                score += 15  # Bonus for smart contrarian
            
            # Penalty for being TOO contrarian (all low owned)
            if avg_own < 5:
                score -= 20
                
        elif self.strategy == "Ceiling Chaser":
            # Emphasize upside over safety
            ceiling_score = sum(p['Ceiling'] for p in players)
            score = ceiling_score * 0.7 + total_proj * 0.3
            
        elif self.strategy == "Correlation Stack":
            # Bonus for correlated players (implemented in stack logic)
            stack_bonus = self._calculate_stack_bonus(players)
            score = score + stack_bonus * self.correlation_focus * 5
        
        return score
    
    def _calculate_stack_bonus(self, players: List[Dict]) -> float:
        """Calculate correlation bonus based on game stacking"""
        if self.sport == "NFL":
            return self._calculate_nfl_stack_bonus(players)
        else:
            return self._calculate_nba_stack_bonus(players)
    
    def _calculate_nfl_stack_bonus(self, players: List[Dict]) -> float:
        """NFL-specific stacking logic"""
        bonus = 0
        
        # QB + Pass catchers from same team
        qb = next((p for p in players if 'QB' in p['Position']), None)
        if qb:
            qb_team = qb['Team']
            pass_catchers = [p for p in players if p['Team'] == qb_team and 
                           any(pos in p['Position'] for pos in ['WR', 'TE'])]
            
            # Primary stack (QB + 1-2 pass catchers)
            if len(pass_catchers) >= 1:
                bonus += 3 * len(pass_catchers)
            
            # Bring-back (player from opposing team)
            if 'Game' in qb:
                opp_team = self._get_opponent(qb)
                bring_backs = [p for p in players if p['Team'] == opp_team]
                if bring_backs:
                    bonus += 2
        
        # RB + DST same team (negative correlation, avoid)
        teams = [p['Team'] for p in players]
        for team in set(teams):
            has_rb = any(p['Team'] == team and 'RB' in p['Position'] for p in players)
            has_dst = any(p['Team'] == team and 'DST' in p['Position'] for p in players)
            if has_rb and has_dst:
                bonus -= 3  # Penalty for poor correlation
        
        return bonus
    
    def _calculate_nba_stack_bonus(self, players: List[Dict]) -> float:
        """NBA-specific stacking logic"""
        bonus = 0
        
        # Team stacks (2-3 players from same team in pace-up spots)
        teams = [p['Team'] for p in players]
        team_counts = pd.Series(teams).value_counts()
        
        for team, count in team_counts.items():
            if count == 2:
                bonus += 1
            elif count == 3:
                bonus += 2.5  # Optimal NBA stack
            elif count >= 4:
                bonus -= 2  # Over-stacking is risky
        
        return bonus
    
    def _get_opponent(self, player: Dict) -> str:
        """Extract opponent team from game string"""
        if 'Game' not in player or pd.isna(player['Game']):
            return None
        
        game = player['Game']
        teams = game.replace('@', ' ').split()
        player_team = player['Team']
        
        for team in teams:
            if team != player_team:
                return team
        return None
    
    def _meets_position_requirements(self, players: List[Dict]) -> bool:
        """Check if lineup meets position requirements"""
        if self.sport == "NFL":
            return self._meets_nfl_requirements(players)
        else:
            return self._meets_nba_requirements(players)
    
    def _meets_nfl_requirements(self, players: List[Dict]) -> bool:
        """Check NFL roster requirements"""
        filled = {'QB': 0, 'RB': 0, 'WR': 0, 'TE': 0, 'DST': 0}
        flex_eligible = []
        
        for p in players:
            pos = p['Position']
            if 'QB' in pos:
                filled['QB'] += 1
            elif 'RB' in pos:
                filled['RB'] += 1
                if filled['RB'] > 2:
                    flex_eligible.append(p)
            elif 'WR' in pos:
                filled['WR'] += 1
                if filled['WR'] > 3:
                    flex_eligible.append(p)
            elif 'TE' in pos:
                filled['TE'] += 1
                if filled['TE'] > 1:
                    flex_eligible.append(p)
            elif 'DST' in pos or 'D/ST' in pos:
                filled['DST'] += 1
        
        # Check core requirements
        if (filled['QB'] == 1 and filled['RB'] >= 2 and 
            filled['WR'] >= 3 and filled['TE'] >= 1 and filled['DST'] == 1):
            
            # Check if we have exactly 9 players with flex
            total_flex_needed = 1
            return len(flex_eligible) >= total_flex_needed
        
        return False
    
    def _meets_nba_requirements(self, players: List[Dict]) -> bool:
        """Check NBA roster requirements"""
        # Simplified - would need full multi-position logic
        positions_filled = [p['Position'] for p in players]
        return len(positions_filled) == 8  # Placeholder
    
    def build_lineups(self, num_lineups: int) -> List[Dict]:
        """
        Build optimal lineups using the selected strategy.
        Returns list of lineup dictionaries with analytics.
        """
        lineups = []
        used_combinations = set()
        
        attempts = 0
        max_attempts = num_lineups * 1000
        
        while len(lineups) < num_lineups and attempts < max_attempts:
            attempts += 1
            
            # Build a lineup using strategy-specific logic
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
        """Build a single lineup using the strategy"""
        if self.sport == "NFL":
            return self._build_nfl_lineup()
        else:
            return self._build_nba_lineup()
    
    def _build_nfl_lineup(self) -> List[Dict]:
        """Build NFL lineup with proper stacking and position logic"""
        lineup = []
        remaining_salary = self.salary_cap
        
        # 1. Select QB (critical decision point)
        qb_pool = self.df[self.df['Position'].str.contains('QB', na=False)].copy()
        qb = self._select_by_strategy(qb_pool, 1)[0]
        lineup.append(qb.to_dict())
        remaining_salary -= qb['Salary']
        
        # 2. Stack with QB (1-2 pass catchers from same team)
        qb_team = qb['Team']
        pass_catcher_pool = self.df[
            (self.df['Team'] == qb_team) &
            (self.df['Position'].str.contains('WR|TE', na=False))
        ].copy()
        
        num_stack = 1 if self.strategy == "Balanced GPP" else 2
        stack = self._select_by_strategy(pass_catcher_pool, min(num_stack, len(pass_catcher_pool)))
        
        for player in stack:
            lineup.append(player.to_dict())
            remaining_salary -= player['Salary']
        
        # 3. Fill remaining positions
        positions_needed = {'RB': 2, 'WR': 3 - len(stack), 'TE': 1 - len(stack), 'DST': 1}
        
        for pos, count in positions_needed.items():
            if count > 0:
                pool = self.df[
                    (self.df['Position'].str.contains(pos, na=False)) &
                    (~self.df['Name'].isin([p['Name'] for p in lineup])) &
                    (self.df['Salary'] <= remaining_salary)
                ].copy()
                
                selected = self._select_by_strategy(pool, min(count, len(pool)))
                
                for player in selected:
                    lineup.append(player.to_dict())
                    remaining_salary -= player['Salary']
        
        # 4. Fill FLEX with best remaining value
        flex_pool = self.df[
            (self.df['Position'].str.contains('RB|WR|TE', na=False)) &
            (~self.df['Name'].isin([p['Name'] for p in lineup])) &
            (self.df['Salary'] <= remaining_salary)
        ].copy()
        
        if not flex_pool.empty and len(lineup) < 9:
            flex = self._select_by_strategy(flex_pool, 1)[0]
            lineup.append(flex.to_dict())
        
        # Validate lineup
        if len(lineup) == 9 and sum(p['Salary'] for p in lineup) <= self.salary_cap:
            if sum(p['Salary'] for p in lineup) >= self.min_salary:
                return lineup
        
        return None
    
    def _build_nba_lineup(self) -> List[Dict]:
        """Build NBA lineup - simplified version"""
        # This would need full multi-position optimization
        # Placeholder for now
        return None
    
    def _select_by_strategy(self, pool: pd.DataFrame, count: int) -> pd.DataFrame:
        """Select players from pool based on strategy"""
        if pool.empty or count == 0:
            return pd.DataFrame()
        
        # Add randomization for diversity
        pool = pool.copy()
        pool['Random'] = np.random.random(len(pool))
        
        if self.strategy == "Balanced GPP":
            # Mix of value and leverage
            pool['Score'] = pool['Value'] * 0.5 + pool['Leverage'] * 0.5 + pool['Random'] * 0.1
            
        elif self.strategy == "Leverage Play":
            # Pure leverage focus
            pool['Score'] = pool['Leverage'] * 0.9 + pool['Random'] * 0.1
            
        elif self.strategy == "Contrarian Core":
            # Boost low ownership, but not too low
            pool['Score'] = (
                pool['Projection'] * 0.6 - 
                pool['Ownership'] * 0.3 + 
                pool['Random'] * 0.1
            )
            
        elif self.strategy == "Ceiling Chaser":
            # Emphasize ceiling
            pool['Score'] = pool['Ceiling'] * 0.7 + pool['Value'] * 0.3
            
        else:  # Correlation Stack or Custom
            pool['Score'] = pool['Projection'] * 0.6 + pool['Value'] * 0.4
        
        # Select top scorers
        return pool.nlargest(count, 'Score')
    
    def _create_lineup_dict(self, players: List[Dict]) -> Dict:
        """Create comprehensive lineup dictionary with analytics"""
        total_salary = sum(p['Salary'] for p in players)
        total_proj = sum(p['Projection'] for p in players)
        avg_own = np.mean([p['Ownership'] for p in players])
        total_leverage = sum(p['Leverage'] for p in players)
        total_ceiling = sum(p.get('Ceiling', p['Projection'] * 1.3) for p in players)
        
        # Calculate optimal score
        optimal_score = self._calculate_optimal_score(players)
        
        # Stack rating
        stack_bonus = self._calculate_stack_bonus(players)
        if stack_bonus > 5:
            stack_rating = "Excellent"
        elif stack_bonus > 2:
            stack_rating = "Good"
        elif stack_bonus > 0:
            stack_rating = "Fair"
        else:
            stack_rating = "Poor"
        
        # Construction notes
        notes = self._generate_construction_notes(players)
        
        # Edge plays
        edges = self._identify_edge_plays(players)
        
        return {
            'players': players,
            'salary': total_salary,
            'projection': total_proj,
            'avg_ownership': avg_own,
            'total_leverage': total_leverage,
            'ceiling': total_ceiling,
            'optimal_score': optimal_score,
            'stack_rating': stack_rating,
            'construction_notes': notes,
            'edge_plays': edges
        }
    
    def _generate_construction_notes(self, players: List[Dict]) -> List[str]:
        """Generate strategic notes about the lineup construction"""
        notes = []
        
        # Ownership distribution
        low_own = [p for p in players if p['Ownership'] < 10]
        high_own = [p for p in players if p['Ownership'] > 25]
        
        if low_own:
            notes.append(f"{len(low_own)} low-owned plays for differentiation")
        if high_own:
            notes.append(f"{len(high_own)} chalk plays for safety floor")
        
        # Stacking
        if self.sport == "NFL":
            qb = next((p for p in players if 'QB' in p['Position']), None)
            if qb:
                stack_mates = [p for p in players if p['Team'] == qb['Team'] and 'QB' not in p['Position']]
                if len(stack_mates) >= 2:
                    notes.append(f"Full {qb['Team']} stack with {len(stack_mates)} pieces")
                elif len(stack_mates) == 1:
                    notes.append(f"Primary {qb['Team']} stack")
        
        # Salary usage
        salary_pct = sum(p['Salary'] for p in players) / self.salary_cap * 100
        notes.append(f"Using {salary_pct:.1f}% of salary cap")
        
        return notes
    
    def _identify_edge_plays(self, players: List[Dict]) -> List[str]:
        """Identify specific edges in the lineup"""
        edges = []
        
        for p in players:
            # High leverage
            if p['Leverage'] > 1.5:
                edges.append(f"{p['Name']}: High leverage ({p['Leverage']:.2f})")
            
            # Great value
            if p['Value'] > 1.0:
                edges.append(f"{p['Name']}: Elite value ({p['Value']:.2f}x)")
            
            # Low owned studs
            if p['Projection'] > 18 and p['Ownership'] < 10:
                edges.append(f"{p['Name']}: Low-owned stud ({p['Ownership']:.1f}%)")
        
        return edges[:5]  # Top 5 edges
    
    def export_for_dk(self, lineups: List[Dict]) -> str:
        """Export lineups in DraftKings CSV format"""
        rows = []
        
        for lineup in lineups:
            if self.sport == "NFL":
                row = self._export_nfl_lineup(lineup)
            else:
                row = self._export_nba_lineup(lineup)
            
            rows.append(row)
        
        # Create CSV
        import io
        output = io.StringIO()
        
        if self.sport == "NFL":
            header = "QB,RB,RB,WR,WR,WR,TE,FLEX,DST\n"
        else:
            header = "PG,SG,SF,PF,C,G,F,UTIL\n"
        
        output.write(header)
        for row in rows:
            output.write(','.join(row) + '\n')
        
        return output.getvalue()
    
    def _export_nfl_lineup(self, lineup: Dict) -> List[str]:
        """Format NFL lineup for DK export"""
        players = lineup['players']
        
        # Sort into positions
        qb = next(p['Name'] for p in players if 'QB' in p['Position'])
        rbs = [p['Name'] for p in players if 'RB' in p['Position']][:2]
        wrs = [p['Name'] for p in players if 'WR' in p['Position']][:3]
        te = next(p['Name'] for p in players if 'TE' in p['Position'])
        dst = next(p['Name'] for p in players if 'DST' in p['Position'] or 'D/ST' in p['Position'])
        
        # Remaining is FLEX
        used = [qb, te, dst] + rbs + wrs
        flex = next(p['Name'] for p in players if p['Name'] not in used)
        
        return [qb, rbs[0], rbs[1], wrs[0], wrs[1], wrs[2], te, flex, dst]
    
    def _export_nba_lineup(self, lineup: Dict) -> List[str]:
        """Format NBA lineup for DK export"""
        # Placeholder
        return []
