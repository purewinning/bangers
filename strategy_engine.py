class StrategyEngine:
    """
    Defines professional DFS tournament strategies.
    Based on patterns used by winning players in high-stakes contests.
    """
    
    def __init__(self, sport: str):
        self.sport = sport
        
        self.strategies = {
            "Balanced GPP": {
                "description": "The workhorse strategy for most GPP contests. Balances safety and upside with smart ownership leverage.",
                "philosophy": "Mix chalk and contrarian plays strategically. Avoid being too safe or too different.",
                "principles": [
                    "Use 2-3 chalk plays (>25% ownership) as anchors",
                    "Include 3-4 value/leverage plays (8-15% ownership)",
                    "Have 2-3 differentiation pieces (<8% ownership)",
                    "Primary stack with QB + 1-2 pass catchers (NFL)",
                    "Target 1.0-1.2 overall lineup leverage",
                    "Salary usage: 97-99% of cap"
                ],
                "target_ownership": "10-15% average",
                "risk_level": "Medium",
                "best_for": "Single-entry main slate contests"
            },
            
            "Leverage Play": {
                "description": "Emphasizes players with high projection-to-ownership ratios. Find market inefficiencies.",
                "philosophy": "The field is wrong on certain players. Exploit mispricing between projection and ownership.",
                "principles": [
                    "Target players with 1.5+ leverage ratio",
                    "Fade overpriced 'name value' chalk",
                    "Include mid-tier options field is underweighting",
                    "Stack game field expects to be low-scoring",
                    "Willing to pay down at 1-2 positions for leverage elsewhere",
                    "Don't chase ownership just to be contrarian"
                ],
                "target_ownership": "8-12% average",
                "risk_level": "Medium-High",
                "best_for": "When ownership projections are available and reliable"
            },
            
            "Contrarian Core": {
                "description": "Build around low-owned core without being stupidly contrarian. Strategic differentiation.",
                "philosophy": "Differentiate where it matters most, not everywhere. Smart contrarian builds.",
                "principles": [
                    "3-5 players under 10% ownership (not 8-9)",
                    "At least 1 'safe' chalk play for stability",
                    "Low-own players must have legitimate upside case",
                    "Avoid being contrarian at positions that don't matter (DST/kicker)",
                    "Don't fade elite options just because they're popular",
                    "Target overlooked game environments, not bad plays"
                ],
                "target_ownership": "7-10% average",
                "risk_level": "High",
                "best_for": "Massive field tournaments (100K+ entries)"
            },
            
            "Ceiling Chaser": {
                "description": "Pure upside plays for tournament-winning ceiling. Sacrifices floor for spike potential.",
                "philosophy": "A min-cash doesn't matter. Build for top 0.1% scores only.",
                "principles": [
                    "Emphasize boom/bust players over consistent scorers",
                    "Target players in favorable game scripts (high totals)",
                    "Include 2-3 risky but explosive options",
                    "Consider players returning from injury with upside",
                    "Full game stacks (QB + 2 pass catchers + RB from game)",
                    "Accept 40% finish rate for 10x upside"
                ],
                "target_ownership": "12-18% average (mix of safe high-own and risky low-own)",
                "risk_level": "Very High",
                "best_for": "Sunday Million, Milly Maker type contests"
            },
            
            "Correlation Stack": {
                "description": "Maximize correlated plays from same game(s). When one hits, multiple hit together.",
                "philosophy": "Lineups win tournaments when multiple pieces from same game go off together.",
                "principles": [
                    "QB + 2 pass catchers + opposing RB (NFL)",
                    "Target highest over/under games",
                    "Include both sides of game for hedging",
                    "Mini-correlations (TE + DST same team for shootout fade)",
                    "Pay attention to Vegas lines and game flow",
                    "Bring-back from opposing team is critical"
                ],
                "target_ownership": "Varies based on game stack popularity",
                "risk_level": "High",
                "best_for": "High-total games with leverage opportunity"
            },
            
            "Custom Blend": {
                "description": "Mix and match elements from multiple strategies based on slate dynamics.",
                "philosophy": "No single strategy fits every slate. Adjust to field and game conditions.",
                "principles": [
                    "Evaluate slate-specific factors",
                    "Identify what field is likely doing",
                    "Exploit slate-specific leverage opportunities",
                    "Consider weather, injuries, and news",
                    "Adjust strategy based on contest size and payout structure",
                    "Be flexible and adaptive"
                ],
                "target_ownership": "Varies",
                "risk_level": "Varies",
                "best_for": "Experienced players who understand the slate deeply"
            }
        }
        
        # Sport-specific strategy notes
        if sport == "NFL":
            self._add_nfl_specifics()
        else:
            self._add_nba_specifics()
    
    def _add_nfl_specifics(self):
        """Add NFL-specific strategy details"""
        nfl_notes = {
            "key_stacks": [
                "Primary: QB + WR/TE from same team",
                "Bring-back: Opposing RB or WR",
                "Full game stack: QB + 2 pass catchers + opposing skill",
                "Mini-stacks: RB + DST or TE + DST (contrarian)"
            ],
            "position_leverage": {
                "QB": "Most important position for leverage. Mid-tier QBs often best value.",
                "RB": "Workhorse backs in good game scripts. Touch volume > talent.",
                "WR": "Target WR1s and slot receivers in high-volume passing offenses.",
                "TE": "Contrarian leverage opportunity. Top 5 or punt.",
                "DST": "Stream matchups. Rarely a leverage point."
            },
            "game_theory": [
                "Everyone stacks the highest total game - find the 2nd best",
                "Road underdogs often overlooked despite pass volume upside",
                "Weather games create massive leverage opportunities",
                "Backup RB scenarios (injury situations) = field overreaction"
            ]
        }
        
        for strategy in self.strategies.values():
            strategy['sport_notes'] = nfl_notes
    
    def _add_nba_specifics(self):
        """Add NBA-specific strategy details"""
        nba_notes = {
            "key_stacks": [
                "Team stacks: 2-3 players from high-pace teams",
                "Opposing stars in potential shootouts",
                "Value plays with increased minutes due to injuries"
            ],
            "position_leverage": {
                "PG": "Usage and minutes are king. Target primary ball handlers.",
                "SG/SF": "Look for wing scorers in up-tempo games.",
                "PF/C": "Bigs against weak interior defenses.",
                "UTIL": "Best value play available regardless of position."
            },
            "game_theory": [
                "Late injury news creates massive leverage",
                "Back-to-back situations often overcorrected by field",
                "Blowout potential (both sides) creates opportunity",
                "Stars in plus matchups at <20% ownership = leverage gold"
            ]
        }
        
        for strategy in self.strategies.values():
            strategy['sport_notes'] = nba_notes
    
    def get_strategy_info(self, strategy_name: str) -> dict:
        """Get detailed information about a specific strategy"""
        if strategy_name not in self.strategies:
            strategy_name = "Balanced GPP"  # Default
        
        return self.strategies[strategy_name]
    
    def get_all_strategies(self) -> dict:
        """Get all available strategies"""
        return self.strategies
    
    def recommend_strategy(self, contest_size: int, entry_fee: int) -> str:
        """Recommend strategy based on contest characteristics"""
        if contest_size > 100000:
            return "Contrarian Core"
        elif contest_size > 50000:
            return "Balanced GPP"
        elif entry_fee > 100:
            return "Leverage Play"
        else:
            return "Balanced GPP"
    
    def get_ownership_targets(self, strategy_name: str) -> dict:
        """Get optimal ownership distribution for a strategy"""
        targets = {
            "Balanced GPP": {
                "chalk_plays": (2, 3),  # Number of plays
                "chalk_ownership": (25, 40),  # Ownership range
                "medium_plays": (3, 4),
                "medium_ownership": (10, 25),
                "contrarian_plays": (2, 3),
                "contrarian_ownership": (0, 10)
            },
            "Leverage Play": {
                "chalk_plays": (1, 2),
                "chalk_ownership": (25, 40),
                "medium_plays": (4, 5),
                "medium_ownership": (8, 20),
                "contrarian_plays": (2, 3),
                "contrarian_ownership": (0, 10)
            },
            "Contrarian Core": {
                "chalk_plays": (1, 1),
                "chalk_ownership": (25, 40),
                "medium_plays": (2, 3),
                "medium_ownership": (10, 20),
                "contrarian_plays": (4, 5),
                "contrarian_ownership": (0, 10)
            },
            "Ceiling Chaser": {
                "chalk_plays": (2, 3),
                "chalk_ownership": (25, 40),
                "medium_plays": (2, 3),
                "medium_ownership": (12, 25),
                "contrarian_plays": (2, 3),
                "contrarian_ownership": (0, 12)
            },
            "Correlation Stack": {
                # More flexible based on game stack popularity
                "chalk_plays": (1, 2),
                "chalk_ownership": (20, 40),
                "medium_plays": (3, 4),
                "medium_ownership": (10, 25),
                "contrarian_plays": (2, 3),
                "contrarian_ownership": (0, 15)
            }
        }
        
        return targets.get(strategy_name, targets["Balanced GPP"])
    
    def validate_lineup_strategy(self, lineup: list, strategy_name: str) -> dict:
        """
        Validate if a lineup matches the intended strategy.
        Returns validation results and suggestions.
        """
        ownership_dist = self._analyze_ownership_distribution(lineup)
        targets = self.get_ownership_targets(strategy_name)
        
        validation = {
            "matches_strategy": True,
            "issues": [],
            "suggestions": []
        }
        
        # Check chalk plays
        if not (targets["chalk_plays"][0] <= ownership_dist["chalk_count"] <= targets["chalk_plays"][1]):
            validation["matches_strategy"] = False
            validation["issues"].append(
                f"Chalk count ({ownership_dist['chalk_count']}) outside target range {targets['chalk_plays']}"
            )
        
        # Check contrarian plays
        if not (targets["contrarian_plays"][0] <= ownership_dist["contrarian_count"] <= targets["contrarian_plays"][1]):
            validation["matches_strategy"] = False
            validation["issues"].append(
                f"Contrarian count ({ownership_dist['contrarian_count']}) outside target range {targets['contrarian_plays']}"
            )
        
        # Strategy-specific validations
        if strategy_name == "Leverage Play":
            avg_leverage = sum(p.get('Leverage', 1) for p in lineup) / len(lineup)
            if avg_leverage < 1.0:
                validation["issues"].append(f"Average leverage ({avg_leverage:.2f}) below 1.0 target")
        
        if strategy_name == "Correlation Stack":
            if not self._has_proper_stack(lineup):
                validation["issues"].append("Missing proper correlation stack")
        
        return validation
    
    def _analyze_ownership_distribution(self, lineup: list) -> dict:
        """Analyze how ownership is distributed in a lineup"""
        chalk_count = sum(1 for p in lineup if p.get('Ownership', 0) > 25)
        medium_count = sum(1 for p in lineup if 10 <= p.get('Ownership', 0) <= 25)
        contrarian_count = sum(1 for p in lineup if p.get('Ownership', 0) < 10)
        
        return {
            "chalk_count": chalk_count,
            "medium_count": medium_count,
            "contrarian_count": contrarian_count,
            "avg_ownership": sum(p.get('Ownership', 0) for p in lineup) / len(lineup)
        }
    
    def _has_proper_stack(self, lineup: list) -> bool:
        """Check if lineup has proper correlation stack"""
        if self.sport == "NFL":
            # Check for QB + pass catcher stack
            qb = next((p for p in lineup if 'QB' in p.get('Position', '')), None)
            if qb:
                qb_team = qb.get('Team')
                stack_count = sum(1 for p in lineup 
                                 if p.get('Team') == qb_team 
                                 and 'QB' not in p.get('Position', ''))
                return stack_count >= 1
        
        return True  # Simplified for now
