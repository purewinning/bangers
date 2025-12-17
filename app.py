import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations
import json
from datetime import datetime
from lineup_builder import LineupBuilder
from strategy_engine import StrategyEngine
from projection_analyzer import ProjectionAnalyzer

st.set_page_config(page_title="DK Pro Tournament Optimizer", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .lineup-box {
        background: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .edge-indicator {
        background: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ DK Pro Tournament Optimizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Single-Entry Tournament Strategies for High-Stakes Contests</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    sport = st.selectbox("Sport", ["NFL", "NBA"])
    
    st.subheader("Upload Projections")
    uploaded_file = st.file_uploader("DraftKings CSV", type=['csv'])
    
    st.subheader("Tournament Strategy")
    strategy = st.selectbox(
        "Build Type",
        [
            "Balanced GPP",
            "Leverage Play", 
            "Contrarian Core",
            "Ceiling Chaser",
            "Correlation Stack",
            "Custom Blend"
        ]
    )
    
    st.subheader("Optimization Settings")
    
    num_lineups = st.slider("Lineups to Generate", 1, 10, 3)
    
    min_salary = st.slider("Min Salary Used", 45000, 50000, 48000, step=100)
    
    ownership_weight = st.slider(
        "Ownership Consideration", 
        0.0, 1.0, 0.7,
        help="Higher = More ownership-aware optimization"
    )
    
    correlation_focus = st.slider(
        "Correlation Emphasis",
        0.0, 1.0, 0.5,
        help="Stack strength and game correlation weight"
    )
    
    leverage_target = st.slider(
        "Leverage Target",
        0.0, 2.0, 1.0, 0.1,
        help="Target leverage ratio (1.0 = ownership-neutral)"
    )

# Main content
if uploaded_file is not None:
    # Load and analyze projections
    df = pd.read_csv(uploaded_file)
    
    analyzer = ProjectionAnalyzer(df, sport)
    analysis = analyzer.analyze()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Players Available", len(df))
    with col2:
        st.metric("Avg Proj. Own%", f"{analysis['avg_ownership']:.1f}%")
    with col3:
        st.metric("Value Plays", analysis['value_count'])
    with col4:
        st.metric("Leverage Opps", analysis['leverage_count'])
    
    # Strategy explanation
    st.subheader(f"📊 {strategy} Strategy")
    strategy_engine = StrategyEngine(sport)
    strategy_info = strategy_engine.get_strategy_info(strategy)
    
    st.info(strategy_info['description'])
    
    with st.expander("Strategy Details"):
        st.markdown(f"**Core Philosophy:** {strategy_info['philosophy']}")
        st.markdown(f"**Key Principles:**")
        for principle in strategy_info['principles']:
            st.markdown(f"- {principle}")
    
    # Build lineups
    if st.button("🚀 Generate Optimal Lineups", type="primary"):
        with st.spinner("Building tournament-winning lineups..."):
            
            builder = LineupBuilder(
                df=df,
                sport=sport,
                strategy=strategy,
                ownership_weight=ownership_weight,
                correlation_focus=correlation_focus,
                leverage_target=leverage_target,
                min_salary=min_salary
            )
            
            lineups = builder.build_lineups(num_lineups)
            
            # Display lineups
            st.subheader("🏆 Optimized Lineups")
            
            for idx, lineup in enumerate(lineups, 1):
                with st.expander(f"Lineup {idx} - Projection: {lineup['projection']:.2f} | Salary: ${lineup['salary']:,} | Ownership: {lineup['avg_ownership']:.1f}%", expanded=(idx==1)):
                    
                    lineup_df = pd.DataFrame(lineup['players'])
                    
                    # Format the display
                    display_cols = ['Name', 'Position', 'Team', 'Salary', 'Projection', 'Ownership%', 'Value', 'Leverage']
                    
                    if sport == "NFL":
                        display_cols.append('Game')
                    
                    st.dataframe(
                        lineup_df[display_cols],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Lineup analytics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Leverage", f"{lineup['total_leverage']:.2f}")
                        st.caption("Target: 0.8-1.2 for single-entry")
                    
                    with col2:
                        st.metric("Ceiling Score", f"{lineup['ceiling']:.1f}")
                        st.caption("90th percentile projection")
                    
                    with col3:
                        st.metric("Stack Quality", lineup['stack_rating'])
                        st.caption("Correlation strength")
                    
                    # Build construction notes
                    st.markdown("**Build Notes:**")
                    for note in lineup['construction_notes']:
                        st.markdown(f"- {note}")
                    
                    # Edge identification
                    if lineup['edge_plays']:
                        st.markdown("**🎯 Edge Plays:**")
                        for edge in lineup['edge_plays']:
                            st.markdown(f'<span class="edge-indicator">{edge}</span>', unsafe_allow_html=True)
            
            # Export functionality
            st.subheader("💾 Export Lineups")
            
            export_format = st.radio("Format", ["DraftKings CSV", "JSON Analysis"])
            
            if export_format == "DraftKings CSV":
                csv_data = builder.export_for_dk(lineups)
                st.download_button(
                    "Download DK CSV",
                    csv_data,
                    "dk_lineups.csv",
                    "text/csv"
                )
            else:
                json_data = json.dumps(lineups, indent=2)
                st.download_button(
                    "Download Analysis JSON",
                    json_data,
                    "lineup_analysis.json",
                    "application/json"
                )

else:
    # Landing page
    st.markdown("""
    ## 🎯 Built for High-Stakes Tournament Success
    
    This optimizer implements the sophisticated strategies used by professional DFS players in single-entry tournaments.
    
    ### Key Features:
    
    **🧠 Professional Strategies**
    - Balanced GPP builds with optimal leverage
    - Contrarian core construction (not stupid contrarian)
    - Ceiling-chasing for large-field tournaments
    - Game correlation and stacking theory
    
    **📈 Advanced Analytics**
    - Ownership-adjusted projections
    - Leverage calculations (projection/ownership ratio)
    - Correlation matrices for stacking
    - Value identification with context
    
    **⚡ Smart Optimization**
    - Avoids chalk traps
    - Identifies leverage opportunities
    - Builds for tournament-winning scores
    - Considers professional build patterns
    
    ### Getting Started:
    1. Upload your DraftKings projection CSV (must include ownership projections)
    2. Select your tournament strategy
    3. Adjust optimization parameters
    4. Generate and analyze optimized lineups
    
    ---
    
    **Note:** This optimizer requires projection data with ownership percentages. 
    Use sources like RotoGrinders, DK's own projections, or your own models.
    """)
    
    with st.expander("📋 Required CSV Format"):
        st.markdown("""
        Your CSV should contain these columns:
        
        **NFL:**
        - Name, Position, Team, Salary, Projection, Ownership
        - Optional: Opponent, Game (e.g., "DAL@NYG")
        
        **NBA:**
        - Name, Position, Team, Salary, Projection, Ownership
        - Optional: Opponent, Minutes
        
        Ownership should be in percentage format (e.g., 15.5 for 15.5%)
        """)
