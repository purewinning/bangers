import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class PortfolioArchetype:
    """Defines a lineup archetype for portfolio construction"""
    name: str
    description: str
    target_sim_roi: Tuple[float, float]  # (min, max)
    ownership_target: Tuple[float, float]  # (min, max) average ownership
    allocation: float  # Percentage of portfolio (0-1)
    philosophy: str

class PortfolioConstructor:
    """
    Advanced portfolio construction using multiple lineup archetypes.
    Builds 3-5 lineups that represent different game theory scenarios.
    """
    
    def __init__(self, contest_type: str = 'classic'):
        self.contest_type = contest_type
        self.archetypes = self._define_archetypes()
        
    def _define_archetypes(self) -> List[PortfolioArchetype]:
        """
        Define the 5 lineup archetypes for portfolio construction.
        Based on professional DFS portfolio theory.
        """
        return [
            PortfolioArchetype(
                name='max_leverage',
                description='Pure contrarian - maximum leverage plays',
                target_sim_roi=(100, 300),
                ownership_target=(0, 35),
                allocation=0.20,  # 1 of 5 lineups
                philosophy='This wins the GPP if my leverage edge is correct'
            ),
            
            PortfolioArchetype(
                name='balanced_leverage',
                description='Mix of leverage + one chalky anchor',
                target_sim_roi=(40, 80),
                ownership_target=(35, 45),
                allocation=0.40,  # 2 of 5 lineups
                philosophy='Core thesis - repeatable edge'
            ),
            
            PortfolioArchetype(
                name='correlation_hedge',
                description='Different stacking pattern than main thesis',
                target_sim_roi=(0, 40),
                ownership_target=(40, 50),
                allocation=0.20,  # 1 of 5 lineups
                philosophy='What if game script differs from my main theory?'
            ),
            
            PortfolioArchetype(
                name='chalk_insurance',
                description='Popular stacks and plays',
                target_sim_roi=(-20, 0),
                ownership_target=(50, 100),
                allocation=0.20,  # 1 of 5 lineups
                philosophy='Defensive lineup - hedge against being too clever'
            )
        ]
    
    def calculate_optimal_exposure(self, player: Dict, leverage: float) -> float:
        """
        Calculate optimal exposure for a player based on leverage.
        
        The Pro's Exposure Logic:
        - Leverage > 5.0: 60% exposure (3 of 5 lineups)
        - Leverage > 2.0: 60% exposure
        - Leverage > 0: 80% exposure (4 of 5 lineups)
        - Leverage < -3.0: 20% exposure (fade but keep some)
        - Else: 40% exposure
        """
        projection = player.get('Projection', 0)
        salary = player.get('Salary', 0)
        value = player.get('Value', 0)
        
        # Base exposure from leverage
        if leverage > 5.0:
            base_exposure = 0.60
        elif leverage > 2.0:
            base_exposure = 0.60
        elif leverage > 0:
            base_exposure = 0.80
        elif leverage < -3.0:
            base_exposure = 0.20  # Fade but keep some exposure
        else:
            base_exposure = 0.40
        
        # Adjustments
        
        # Elite punt plays (high value, low salary)
        if value > 2.0 and salary < 3000:
            base_exposure += 0.20
        
        # Slate's best player
        if projection > 20.0:
            base_exposure = min(base_exposure + 0.20, 0.80)
        
        # Cap exposure
        return min(base_exposure, 0.80)
    
    def build_portfolio(self, lineup_pool: List[Dict], 
                       num_lineups: int = 5,
                       sim_results: Dict = None) -> List[Dict]:
        """
        Select optimal portfolio from lineup pool.
        
        Portfolio selection algorithm:
        1. Match lineups to archetype targets
        2. Minimize overlap (manage duplicates)
        3. Maximize expected ROI across portfolio
        4. Ensure proper exposure to key leverage plays
        """
        if len(lineup_pool) < num_lineups:
            return lineup_pool
        
        selected_lineups = []
        
        # Sort lineup pool by sim_roi
        sorted_pool = sorted(lineup_pool, 
                           key=lambda x: x.get('sim_roi', 0), 
                           reverse=True)
        
        # Step 1: Select one MAX LEVERAGE lineup (highest sim ROI)
        max_lev = sorted_pool[0]
        selected_lineups.append(max_lev)
        
        # Step 2: Select two BALANCED LEVERAGE lineups
        balanced = [l for l in sorted_pool 
                   if 40 < l.get('sim_roi', 0) < 80
                   and self._calculate_overlap(l, selected_lineups) < 6]
        
        if len(balanced) >= 2:
            selected_lineups.extend(balanced[:2])
        else:
            # Fallback: take next best
            selected_lineups.extend([l for l in sorted_pool 
                                    if l not in selected_lineups][:2])
        
        # Step 3: Select one CORRELATION HEDGE
        # Different stacking pattern than max leverage
        max_lev_stack = self._identify_stack_pattern(max_lev)
        hedge = [l for l in sorted_pool
                if self._identify_stack_pattern(l) != max_lev_stack
                and l not in selected_lineups
                and self._calculate_overlap(l, selected_lineups) < 6]
        
        if hedge:
            selected_lineups.append(hedge[0])
        else:
            # Fallback
            selected_lineups.append([l for l in sorted_pool 
                                    if l not in selected_lineups][0])
        
        # Step 4: Select one CHALK INSURANCE
        # Higher ownership lineup
        chalk = [l for l in sorted_pool
                if l.get('avg_ownership', 0) > 50
                and l not in selected_lineups]
        
        if chalk:
            # Pick chalk lineup with lowest sim_roi (most defensive)
            selected_lineups.append(min(chalk, key=lambda x: x.get('sim_roi', 0)))
        else:
            # Fallback
            remaining = [l for l in sorted_pool if l not in selected_lineups]
            if remaining:
                selected_lineups.append(remaining[0])
        
        return selected_lineups[:num_lineups]
    
    def calculate_duplicate_targets(self, portfolio_size: int = 5) -> Dict:
        """
        Calculate target duplicate distribution.
        
        The pro's duplicate distribution: 0, 1, 4, 5, 10
        This represents:
        - 1 unique lineup (0 duplicates)
        - 1 slightly different (1-2 duplicates)
        - 2 similar core constructions (4-6 duplicates)
        - 1 heavy on favorite build (8-10 duplicates)
        """
        if portfolio_size == 3:
            return {
                'lineup_1': {'max_duplicates': 0, 'uniqueness': 'maximum'},
                'lineup_2': {'max_duplicates': 3, 'uniqueness': 'medium'},
                'lineup_3': {'max_duplicates': 8, 'uniqueness': 'low'}
            }
        elif portfolio_size == 5:
            return {
                'lineup_1': {'max_duplicates': 0, 'uniqueness': 'maximum'},
                'lineup_2': {'max_duplicates': 2, 'uniqueness': 'high'},
                'lineup_3': {'max_duplicates': 5, 'uniqueness': 'medium'},
                'lineup_4': {'max_duplicates': 6, 'uniqueness': 'medium'},
                'lineup_5': {'max_duplicates': 10, 'uniqueness': 'low'}
            }
        else:
            # Default strategy
            return {f'lineup_{i+1}': {
                'max_duplicates': i * 2, 
                'uniqueness': 'varied'
            } for i in range(portfolio_size)}
    
    def validate_exposure(self, portfolio: List[Dict], 
                         target_exposures: Dict) -> Dict:
        """
        Validate that portfolio meets exposure targets.
        Returns exposure analysis.
        """
        # Count player appearances
        player_counts = {}
        total_lineups = len(portfolio)
        
        for lineup in portfolio:
            for player in lineup['players']:
                name = player['Name']
                player_counts[name] = player_counts.get(name, 0) + 1
        
        # Calculate actual vs target exposure
        exposure_analysis = {}
        
        for player, count in player_counts.items():
            actual_exposure = count / total_lineups
            target_exposure = target_exposures.get(player, 0.40)  # Default 40%
            
            exposure_analysis[player] = {
                'actual': actual_exposure,
                'target': target_exposure,
                'difference': actual_exposure - target_exposure,
                'status': 'on_target' if abs(actual_exposure - target_exposure) < 0.10 else 'off_target'
            }
        
        return exposure_analysis
    
    def _calculate_overlap(self, lineup: Dict, portfolio: List[Dict]) -> int:
        """Calculate average player overlap between lineup and portfolio"""
        if not portfolio:
            return 0
        
        lineup_players = set(p['Name'] for p in lineup['players'])
        
        overlaps = []
        for existing_lineup in portfolio:
            existing_players = set(p['Name'] for p in existing_lineup['players'])
            overlap = len(lineup_players & existing_players)
            overlaps.append(overlap)
        
        return int(np.mean(overlaps))
    
    def _identify_stack_pattern(self, lineup: Dict) -> str:
        """Identify the stacking pattern used in a lineup"""
        players = lineup['players']
        
        # Count players by team
        teams = {}
        for player in players:
            team = player.get('Team', 'UNK')
            teams[team] = teams.get(team, [])
            teams[team].append(player.get('Position', ''))
        
        # Identify pattern
        for team, positions in teams.items():
            if len(positions) >= 3:
                if 'QB' in positions:
                    return f'qb_primary_{team}'
                else:
                    return f'rb_game_script_{team}'
        
        return 'balanced'
    
    def generate_portfolio_report(self, portfolio: List[Dict]) -> str:
        """Generate a detailed portfolio report"""
        report = []
        report.append("=" * 70)
        report.append("PORTFOLIO CONSTRUCTION REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Portfolio summary
        total_roi = sum(l.get('sim_roi', 0) for l in portfolio) / len(portfolio)
        avg_ownership = sum(l.get('avg_ownership', 0) for l in portfolio) / len(portfolio)
        
        report.append(f"Portfolio Size: {len(portfolio)} lineups")
        report.append(f"Expected ROI: {total_roi:.1f}%")
        report.append(f"Average Ownership: {avg_ownership:.1f}%")
        report.append("")
        
        # Individual lineups
        for idx, lineup in enumerate(portfolio, 1):
            archetype = self._classify_lineup(lineup)
            report.append(f"Lineup {idx}: {archetype.upper()}")
            report.append(f"  Sim ROI: {lineup.get('sim_roi', 0):.1f}%  |  " +
                         f"Own Sum: {lineup.get('avg_ownership', 0):.1f}%  |  " +
                         f"Duplicates: {lineup.get('duplicates', 0)}")
            
            # Key players
            sorted_players = sorted(
                lineup['players'], 
                key=lambda x: x.get('Leverage', 0), 
                reverse=True
            )[:3]
            
            for player in sorted_players:
                report.append(f"  ├─ {player['Name']} ({player.get('Position', 'UNK')}) - " +
                             f"Leverage: {player.get('Leverage', 0):+.2f}%")
            
            report.append("")
        
        # Exposure summary
        report.append("-" * 70)
        report.append("PLAYER EXPOSURE MATRIX")
        report.append("-" * 70)
        
        # Count exposures
        player_exposure = {}
        for lineup in portfolio:
            for player in lineup['players']:
                name = player['Name']
                player_exposure[name] = player_exposure.get(name, 0) + 1
        
        # Sort by exposure
        sorted_exposure = sorted(
            player_exposure.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        for player, count in sorted_exposure:
            exposure_pct = (count / len(portfolio)) * 100
            bars = "█" * count + "░" * (len(portfolio) - count)
            report.append(f"{player:25s} | {bars} | {exposure_pct:5.0f}%")
        
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def _classify_lineup(self, lineup: Dict) -> str:
        """Classify lineup into an archetype"""
        sim_roi = lineup.get('sim_roi', 0)
        avg_own = lineup.get('avg_ownership', 0)
        
        if sim_roi > 100:
            return 'max_leverage'
        elif 40 <= sim_roi <= 80:
            return 'balanced_leverage'
        elif 0 <= sim_roi < 40:
            return 'correlation_hedge'
        else:
            return 'chalk_insurance'
    
    def calculate_portfolio_metrics(self, portfolio: List[Dict]) -> Dict:
        """Calculate comprehensive portfolio metrics"""
        if not portfolio:
            return {}
        
        return {
            'portfolio_size': len(portfolio),
            'expected_roi': sum(l.get('sim_roi', 0) for l in portfolio) / len(portfolio),
            'avg_ownership': sum(l.get('avg_ownership', 0) for l in portfolio) / len(portfolio),
            'total_leverage': sum(l.get('total_leverage', 0) for l in portfolio) / len(portfolio),
            'avg_ceiling': sum(l.get('ceiling', 0) for l in portfolio) / len(portfolio),
            'top_1_percent_rate': sum(l.get('top_1_percent_rate', 0) for l in portfolio) / len(portfolio),
            'min_cash_rate': sum(l.get('min_cash_rate', 0) for l in portfolio) / len(portfolio),
            'uniqueness_score': self._calculate_uniqueness(portfolio),
            'archetype_distribution': self._analyze_archetypes(portfolio)
        }
    
    def _calculate_uniqueness(self, portfolio: List[Dict]) -> float:
        """Calculate how unique/diverse the portfolio is"""
        if len(portfolio) < 2:
            return 1.0
        
        overlaps = []
        for i, lineup1 in enumerate(portfolio):
            for lineup2 in portfolio[i+1:]:
                players1 = set(p['Name'] for p in lineup1['players'])
                players2 = set(p['Name'] for p in lineup2['players'])
                overlap = len(players1 & players2)
                overlaps.append(overlap)
        
        avg_overlap = np.mean(overlaps)
        max_possible_overlap = len(portfolio[0]['players'])
        
        # Uniqueness score: 1.0 = totally unique, 0.0 = all identical
        uniqueness = 1.0 - (avg_overlap / max_possible_overlap)
        return uniqueness
    
    def _analyze_archetypes(self, portfolio: List[Dict]) -> Dict:
        """Analyze archetype distribution in portfolio"""
        archetypes = {}
        for lineup in portfolio:
            archetype = self._classify_lineup(lineup)
            archetypes[archetype] = archetypes.get(archetype, 0) + 1
        
        return archetypes
