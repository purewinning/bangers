import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class SimulationResult:
    """Results from Monte Carlo simulation"""
    player: str
    mean_score: float
    std_dev: float
    percentile_10: float
    percentile_50: float
    percentile_90: float
    ceiling: float
    floor: float
    optimal_rate: float  # Appearance rate in top 1% lineups

class MonteCarloEngine:
    """
    Monte Carlo simulation engine for DFS portfolio optimization.
    Generates 10,000+ simulations to model score distributions and leverage.
    """
    
    def __init__(self, num_simulations: int = 10000):
        self.num_simulations = num_simulations
        self.sim_results = {}
        
    def simulate_player_scores(self, df: pd.DataFrame) -> Dict[str, SimulationResult]:
        """
        Simulate each player's performance distribution.
        Uses projection + std dev to generate realistic score ranges.
        """
        results = {}
        
        for _, player in df.iterrows():
            name = player['Name']
            projection = player['Projection']
            
            # Use provided Std Dev or estimate
            if 'StdDev' in player and pd.notna(player['StdDev']):
                std_dev = player['StdDev']
            else:
                # Estimate: ~25% of projection for most players
                std_dev = projection * 0.25
            
            # Generate simulations using normal distribution
            simulated_scores = np.random.normal(
                loc=projection,
                scale=std_dev,
                size=self.num_simulations
            )
            
            # Ensure non-negative scores
            simulated_scores = np.maximum(simulated_scores, 0)
            
            results[name] = SimulationResult(
                player=name,
                mean_score=float(np.mean(simulated_scores)),
                std_dev=float(np.std(simulated_scores)),
                percentile_10=float(np.percentile(simulated_scores, 10)),
                percentile_50=float(np.percentile(simulated_scores, 50)),
                percentile_90=float(np.percentile(simulated_scores, 90)),
                ceiling=float(np.percentile(simulated_scores, 95)),
                floor=float(np.percentile(simulated_scores, 5)),
                optimal_rate=0.0  # Calculated later
            )
        
        self.sim_results = results
        return results
    
    def simulate_lineup_scores(self, lineups: List[List[Dict]], 
                               correlation_matrix: Dict = None) -> List[Dict]:
        """
        Simulate each lineup's score distribution across all simulations.
        Accounts for correlation between players.
        """
        lineup_sims = []
        
        for lineup in lineups:
            scores = np.zeros(self.num_simulations)
            
            for player_dict in lineup:
                player_name = player_dict['Name']
                projection = player_dict['Projection']
                
                # Get std dev
                if 'StdDev' in player_dict and pd.notna(player_dict['StdDev']):
                    std_dev = player_dict['StdDev']
                else:
                    std_dev = projection * 0.25
                
                # Simulate player scores
                player_scores = np.random.normal(projection, std_dev, self.num_simulations)
                player_scores = np.maximum(player_scores, 0)
                
                # Add correlation if applicable (QB-WR same team, etc.)
                if correlation_matrix:
                    player_scores = self._apply_correlation(
                        player_scores, player_dict, lineup, correlation_matrix
                    )
                
                scores += player_scores
            
            # Calculate lineup metrics
            lineup_sim = {
                'lineup': lineup,
                'mean_score': float(np.mean(scores)),
                'std_dev': float(np.std(scores)),
                'ceiling': float(np.percentile(scores, 90)),
                'floor': float(np.percentile(scores, 10)),
                'top_1_percent_score': float(np.percentile(scores, 99)),
                'min_cash_score': float(np.percentile(scores, 80)),
                'score_distribution': scores
            }
            
            lineup_sims.append(lineup_sim)
        
        return lineup_sims
    
    def calculate_optimal_rates(self, lineup_pool: List[Dict], 
                                top_percent: float = 0.01) -> Dict[str, float]:
        """
        Calculate optimal rate for each player.
        Optimal% = How often player appears in top X% of simulated lineups.
        """
        # Simulate all lineups
        lineup_scores = []
        for lineup_data in lineup_pool:
            lineup = lineup_data['players']
            
            # Calculate mean score for this lineup
            total_proj = sum(p['Projection'] for p in lineup)
            lineup_scores.append({
                'score': total_proj,
                'players': [p['Name'] for p in lineup]
            })
        
        # Sort by score
        lineup_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Find top X%
        cutoff = int(len(lineup_scores) * top_percent)
        top_lineups = lineup_scores[:cutoff]
        
        # Count player appearances in top lineups
        player_appearances = {}
        total_top_lineups = len(top_lineups)
        
        for lineup in top_lineups:
            for player in lineup['players']:
                player_appearances[player] = player_appearances.get(player, 0) + 1
        
        # Calculate optimal rate
        optimal_rates = {}
        for player, count in player_appearances.items():
            optimal_rates[player] = count / total_top_lineups if total_top_lineups > 0 else 0
        
        return optimal_rates
    
    def simulate_contest_finish(self, lineup: List[Dict], 
                                field_size: int = 10000,
                                ownership_data: Dict = None) -> Dict:
        """
        Simulate where this lineup finishes in a contest.
        Returns finish distribution and expected ROI.
        """
        lineup_scores = []
        
        # Simulate this lineup many times
        for _ in range(self.num_simulations):
            score = 0
            for player in lineup:
                projection = player['Projection']
                std_dev = player.get('StdDev', projection * 0.25)
                player_score = np.random.normal(projection, std_dev)
                score += max(0, player_score)
            
            lineup_scores.append(score)
        
        # Simulate field (simplified - uses ownership to determine field construction)
        field_scores = self._simulate_field(field_size, ownership_data)
        
        # Calculate finish positions
        finishes = []
        for lineup_score in lineup_scores:
            # Count how many field lineups beat this score
            finish = sum(1 for fs in field_scores if fs > lineup_score) + 1
            finishes.append(finish)
        
        # Calculate metrics
        avg_finish = np.mean(finishes)
        top_1_percent_rate = sum(1 for f in finishes if f <= field_size * 0.01) / len(finishes)
        top_10_percent_rate = sum(1 for f in finishes if f <= field_size * 0.10) / len(finishes)
        min_cash_rate = sum(1 for f in finishes if f <= field_size * 0.20) / len(finishes)
        
        return {
            'avg_finish': avg_finish,
            'top_1_percent_rate': top_1_percent_rate * 100,
            'top_10_percent_rate': top_10_percent_rate * 100,
            'min_cash_rate': min_cash_rate * 100,
            'finish_distribution': finishes,
            'score_distribution': lineup_scores
        }
    
    def _simulate_field(self, field_size: int, ownership_data: Dict) -> List[float]:
        """
        Simulate the entire field's score distribution.
        Uses ownership to determine field construction patterns.
        """
        # Simplified field simulation
        # In production, this would model actual field construction
        field_scores = []
        
        for _ in range(min(field_size, 1000)):  # Sample for efficiency
            # Generate a field lineup based on ownership
            score = np.random.normal(100, 20)  # Simplified
            field_scores.append(max(0, score))
        
        return field_scores
    
    def _apply_correlation(self, player_scores: np.ndarray, 
                          player: Dict, lineup: List[Dict],
                          correlation_matrix: Dict) -> np.ndarray:
        """
        Apply correlation between players (QB-WR, RB-DST, etc.)
        """
        # Check for correlations
        player_team = player.get('Team')
        player_pos = player.get('Position', '')
        
        for other_player in lineup:
            if other_player['Name'] == player['Name']:
                continue
            
            other_team = other_player.get('Team')
            other_pos = other_player.get('Position', '')
            
            # Positive correlation: QB-WR/TE same team
            if (player_team == other_team and 
                ('QB' in player_pos and any(p in other_pos for p in ['WR', 'TE'])) or
                ('QB' in other_pos and any(p in player_pos for p in ['WR', 'TE']))):
                # Add positive correlation (simplified)
                correlation_factor = 0.3
                player_scores = player_scores * (1 + correlation_factor * 0.1)
            
            # Negative correlation: RB-DST same team
            if (player_team == other_team and
                ('RB' in player_pos and 'DST' in other_pos) or
                ('RB' in other_pos and 'DST' in player_pos)):
                # Add negative correlation
                correlation_factor = -0.2
                player_scores = player_scores * (1 + correlation_factor * 0.1)
        
        return player_scores
    
    def calculate_leverage(self, player_name: str, 
                          optimal_rate: float, 
                          ownership: float) -> float:
        """
        Calculate leverage for a player.
        Leverage = Optimal% - Ownership%
        
        Positive leverage = Player appears in winning lineups MORE than ownership suggests
        Negative leverage = Overowned relative to win probability
        """
        return optimal_rate - ownership
    
    def generate_correlation_matrix(self, df: pd.DataFrame) -> Dict:
        """
        Generate correlation matrix for players.
        Used to model how players' scores correlate in simulations.
        """
        correlation_matrix = {}
        
        # QB-WR/TE same team: +0.65 correlation
        # QB-RB same team: -0.15 correlation
        # RB-DST same team: -0.30 correlation
        # Opposing offensive players: +0.20 correlation (shootout)
        
        for _, player1 in df.iterrows():
            correlations = {}
            
            for _, player2 in df.iterrows():
                if player1['Name'] == player2['Name']:
                    continue
                
                # Calculate correlation based on positions and teams
                corr = self._calculate_position_correlation(player1, player2)
                correlations[player2['Name']] = corr
            
            correlation_matrix[player1['Name']] = correlations
        
        return correlation_matrix
    
    def _calculate_position_correlation(self, player1: pd.Series, 
                                       player2: pd.Series) -> float:
        """
        Calculate correlation coefficient between two players.
        """
        team1 = player1.get('Team', '')
        team2 = player2.get('Team', '')
        pos1 = player1.get('Position', '')
        pos2 = player2.get('Position', '')
        
        # Same team correlations
        if team1 == team2:
            # QB-WR/TE: Strong positive
            if ('QB' in pos1 and any(p in pos2 for p in ['WR', 'TE'])) or \
               ('QB' in pos2 and any(p in pos1 for p in ['WR', 'TE'])):
                return 0.65
            
            # QB-RB: Slight negative
            if ('QB' in pos1 and 'RB' in pos2) or ('QB' in pos2 and 'RB' in pos1):
                return -0.15
            
            # RB-DST: Negative
            if ('RB' in pos1 and 'DST' in pos2) or ('RB' in pos2 and 'DST' in pos1):
                return -0.30
            
            # WR-WR: Slight negative (target competition)
            if 'WR' in pos1 and 'WR' in pos2:
                return -0.10
        
        # Opposing teams (same game)
        else:
            # Check if same game
            if player1.get('Opponent') == team2 or player2.get('Opponent') == team1:
                # Offensive players in shootout
                if all(p not in pos1 + pos2 for p in ['DST']):
                    return 0.20
        
        # Default: no correlation
        return 0.0
