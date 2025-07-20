import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils import load_data, filter_data, create_player_profile, create_team_comparison

# Import new functions with fallback for deployment environments
try:
    from utils import create_multi_player_profile, create_stat_comparison_chart
except ImportError:
    # Fallback functions for deployment environments that haven't updated yet
    def create_multi_player_profile(player_data):
        """Fallback function for multi-player profile"""
        return create_player_profile(player_data)
    
    def create_stat_comparison_chart(player_data, stat_name):
        """Fallback function for stat comparison chart"""
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_annotation(text="Comparison chart not available", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

# Page configuration
st.set_page_config(
    page_title="CJFL Analytics Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stApp {
        background-color: #0e1117;
    }
    .stSidebar {
        background-color: #262730;
    }
    .stSelectbox, .stTextInput {
        background-color: #262730;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #464646;
        margin: 0.5rem 0;
    }
    .player-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #464646;
        margin: 1rem 0;
    }
    .player-card-1 { border-left: 4px solid #ff6384; }
    .player-card-2 { border-left: 4px solid #36a2eb; }
    .player-card-3 { border-left: 4px solid #ffcd56; }
    .player-card-4 { border-left: 4px solid #4bc0c0; }
    .player-card-5 { border-left: 4px solid #9966ff; }
    h1, h2, h3 {
        color: #fafafa;
        font-weight: bold;
    }
    .stMetric {
        background-color: #262730;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_cached_data():
    return load_data()

data = load_cached_data()

# Header
st.title("🏈 CJFL Analytics Dashboard")
st.markdown("**Canadian Junior Football League Player Statistics (2024 Season)**")

# Data source indicator
if not data.empty:
    total_players = len(data['Player Name'].unique())
    total_teams = len(data['Team'].unique())
    
    if total_teams >= 8:
        st.success(f"✅ Real CJFL Data: {total_players} players from {total_teams} teams")
    elif total_teams >= 4:
        st.warning(f"⚠️ Partial Real Data: {total_players} players from {total_teams} teams")
    else:
        st.info(f"📊 Sample Data: {total_players} players from {total_teams} teams")
else:
    st.error("❌ No data available")

# Sidebar filters
st.sidebar.header("📊 Filters")

# Season filter (2024 only)
selected_seasons = [2024]

# Team filter
all_teams = sorted(data['Team'].unique())
selected_teams = st.sidebar.multiselect(
    "Select Teams",
    options=all_teams,
    default=all_teams
)

# Position filter
all_positions = sorted(data['Position'].unique())
selected_positions = st.sidebar.multiselect(
    "Select Positions",
    options=all_positions,
    default=all_positions
)

# Player search
player_search = st.sidebar.text_input("Search Player", "")

# Filter data based on selections
filtered_data = filter_data(data, selected_seasons, selected_teams, selected_positions, player_search)

# Main content
if filtered_data.empty:
    st.warning("No data matches your current filters. Please adjust your selections.")
else:
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(filtered_data['Player Name'].unique()))
    
    with col2:
        st.metric("Total Teams", len(filtered_data['Team'].unique()))
    
    with col3:
        st.metric("Total Touchdowns", int(filtered_data['Touchdowns'].sum()))
    
    with col4:
        st.metric("Total Yards", f"{int(filtered_data[['Passing Yards', 'Rushing Yards', 'Receiving Yards']].sum().sum()):,}")

    # Top 10 Players by Stat Category
    st.header("🏆 Top 10 Players by Category")
    
    # Calculate additional statistics
    filtered_data['Total Yards'] = filtered_data['Passing Yards'] + filtered_data['Rushing Yards'] + filtered_data['Receiving Yards']
    filtered_data['Total Offensive Yards'] = filtered_data['Rushing Yards'] + filtered_data['Receiving Yards']
    filtered_data['Yards per Game'] = filtered_data['Total Yards'] / filtered_data['Games Played']
    filtered_data['Touchdowns per Game'] = filtered_data['Touchdowns'] / filtered_data['Games Played']
    filtered_data['Tackles per Game'] = filtered_data['Tackles'] / filtered_data['Games Played']
    filtered_data['Sacks per Game'] = filtered_data['Sacks'] / filtered_data['Games Played']
    
    # Create tabs for all stat categories
    stat_tabs = st.tabs([
        "Passing Yards", "Rushing Yards", "Receiving Yards", "Total Yards", "Total Offensive Yards",
        "Touchdowns", "Touchdowns per Game", "Tackles", "Tackles per Game", "Sacks", "Sacks per Game",
        "Yards per Game", "Games Played"
    ])
    
    stat_columns = {
        "Passing Yards": "Passing Yards",
        "Rushing Yards": "Rushing Yards", 
        "Receiving Yards": "Receiving Yards",
        "Total Yards": "Total Yards",
        "Total Offensive Yards": "Total Offensive Yards",
        "Touchdowns": "Touchdowns",
        "Touchdowns per Game": "Touchdowns per Game",
        "Tackles": "Tackles",
        "Tackles per Game": "Tackles per Game",
        "Sacks": "Sacks",
        "Sacks per Game": "Sacks per Game",
        "Yards per Game": "Yards per Game",
        "Games Played": "Games Played"
    }
    
    for tab, (tab_name, column) in zip(stat_tabs, stat_columns.items()):
        with tab:
            # Handle per-game stats that might have NaN values
            if 'per Game' in column:
                valid_data = filtered_data[filtered_data[column].notna()]
                top_players = valid_data.nlargest(10, column)[['Player Name', 'Team', 'Position', column]]
            else:
                top_players = filtered_data.nlargest(10, column)[['Player Name', 'Team', 'Position', column]]
            
            if not top_players.empty:
                fig = px.bar(
                    top_players,
                    x=column,
                    y='Player Name',
                    color='Team',
                    orientation='h',
                    title=f"Top 10 Players by {tab_name}",
                    labels={column: tab_name, 'Player Name': 'Player'},
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#fafafa'),
                    xaxis=dict(gridcolor='#464646'),
                    yaxis=dict(gridcolor='#464646')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display detailed table
                st.subheader("📋 Detailed Rankings")
                display_data = top_players.copy()
                if column in ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Total Yards', 'Total Offensive Yards']:
                    display_data[column] = display_data[column].apply(lambda x: f"{int(x):,}")
                elif 'per Game' in column:
                    display_data[column] = display_data[column].apply(lambda x: f"{x:.2f}")
                else:
                    display_data[column] = display_data[column].apply(lambda x: f"{int(x)}")
                
                st.dataframe(display_data, use_container_width=True)
            else:
                st.info(f"No valid data available for {tab_name}")

    # Player Performance Analysis
    st.header("📊 Player Performance Analysis")
    
    # Player selector for analysis
    unique_players = sorted(filtered_data['Player Name'].unique())
    selected_player_analysis = st.selectbox(
        "Select Player for Performance Analysis",
        options=unique_players,
        index=0 if unique_players else None
    )
    
    if selected_player_analysis:
        player_analysis_data = filtered_data[filtered_data['Player Name'] == selected_player_analysis]
        
        if not player_analysis_data.empty:
            player_info = player_analysis_data.iloc[0]
            
            # Calculate additional stats for the selected player
            total_yards = player_info['Passing Yards'] + player_info['Rushing Yards'] + player_info['Receiving Yards']
            total_offensive_yards = player_info['Rushing Yards'] + player_info['Receiving Yards']
            yards_per_game = total_yards / player_info['Games Played'] if player_info['Games Played'] > 0 else 0
            touchdowns_per_game = player_info['Touchdowns'] / player_info['Games Played'] if player_info['Games Played'] > 0 else 0
            tackles_per_game = player_info['Tackles'] / player_info['Games Played'] if player_info['Games Played'] > 0 else 0
            sacks_per_game = player_info['Sacks'] / player_info['Games Played'] if player_info['Games Played'] > 0 else 0
            
            # Create comprehensive performance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Yards", f"{int(total_yards):,}")
                st.metric("Yards per Game", f"{yards_per_game:.1f}")
            
            with col2:
                st.metric("Touchdowns", int(player_info['Touchdowns']))
                st.metric("TDs per Game", f"{touchdowns_per_game:.2f}")
            
            with col3:
                st.metric("Tackles", int(player_info['Tackles']))
                st.metric("Tackles per Game", f"{tackles_per_game:.2f}")
            
            with col4:
                st.metric("Sacks", int(player_info['Sacks']))
                st.metric("Sacks per Game", f"{sacks_per_game:.2f}")
            
            # Create subplot for comprehensive stats
            fig = make_subplots(
                rows=3, cols=3,
                subplot_titles=(
                    'Passing Yards', 'Rushing Yards', 'Receiving Yards',
                    'Touchdowns', 'Tackles', 'Sacks',
                    'Total Yards', 'Games Played', 'Total Offensive Yards'
                ),
                specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
            )
            
            stats_to_plot = [
                'Passing Yards', 'Rushing Yards', 'Receiving Yards',
                'Touchdowns', 'Tackles', 'Sacks',
                'Total Yards', 'Games Played', 'Total Offensive Yards'
            ]
            positions = [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)]
            
            for stat, pos in zip(stats_to_plot, positions):
                if stat == 'Total Yards':
                    value = total_yards
                elif stat == 'Total Offensive Yards':
                    value = total_offensive_yards
                else:
                    value = player_info[stat]
                
                fig.add_trace(
                    go.Bar(
                        x=[stat],
                        y=[value],
                        name=stat,
                        showlegend=False
                    ),
                    row=pos[0], col=pos[1]
                )
            
            fig.update_layout(
                title=f"Comprehensive Performance Analysis for {selected_player_analysis} (2024 Season)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                height=800
            )
            
            fig.update_xaxes(gridcolor='#464646')
            fig.update_yaxes(gridcolor='#464646')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed statistics table
            st.subheader("📋 Detailed Player Statistics")
            
            detailed_stats = {
                'Basic Info': {
                    'Player Name': player_info['Player Name'],
                    'Team': player_info['Team'],
                    'Position': player_info['Position'],
                    'Games Played': int(player_info['Games Played'])
                },
                'Offensive Stats': {
                    'Passing Yards': f"{int(player_info['Passing Yards']):,}",
                    'Rushing Yards': f"{int(player_info['Rushing Yards']):,}",
                    'Receiving Yards': f"{int(player_info['Receiving Yards']):,}",
                    'Total Yards': f"{int(total_yards):,}",
                    'Total Offensive Yards': f"{int(total_offensive_yards):,}",
                    'Touchdowns': int(player_info['Touchdowns'])
                },
                'Defensive Stats': {
                    'Tackles': int(player_info['Tackles']),
                    'Sacks': int(player_info['Sacks']),
                    'Interceptions': int(player_info['Interceptions'])
                },
                'Per Game Averages': {
                    'Yards per Game': f"{yards_per_game:.1f}",
                    'Touchdowns per Game': f"{touchdowns_per_game:.2f}",
                    'Tackles per Game': f"{tackles_per_game:.2f}",
                    'Sacks per Game': f"{sacks_per_game:.2f}"
                }
            }
            
            # Display stats in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Basic Info**")
                for key, value in detailed_stats['Basic Info'].items():
                    st.write(f"{key}: {value}")
                
                st.write("**Offensive Stats**")
                for key, value in detailed_stats['Offensive Stats'].items():
                    st.write(f"{key}: {value}")
            
            with col2:
                st.write("**Defensive Stats**")
                for key, value in detailed_stats['Defensive Stats'].items():
                    st.write(f"{key}: {value}")
                
                st.write("**Per Game Averages**")
                for key, value in detailed_stats['Per Game Averages'].items():
                    st.write(f"{key}: {value}")

    # Team vs Team Comparison
    st.header("🏆 Team Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        team1 = st.selectbox("Select Team 1", options=sorted(filtered_data['Team'].unique()))
    
    with col2:
        team2 = st.selectbox("Select Team 2", options=sorted(filtered_data['Team'].unique()), index=1 if len(filtered_data['Team'].unique()) > 1 else 0)
    
    if team1 and team2:
        # Create comprehensive team comparison
        team1_data = filtered_data[filtered_data['Team'] == team1]
        team2_data = filtered_data[filtered_data['Team'] == team2]
        
        # Calculate team statistics
        team1_stats = {
            'Total Yards': team1_data[['Passing Yards', 'Rushing Yards', 'Receiving Yards']].sum().sum(),
            'Passing Yards': team1_data['Passing Yards'].sum(),
            'Rushing Yards': team1_data['Rushing Yards'].sum(),
            'Receiving Yards': team1_data['Receiving Yards'].sum(),
            'Touchdowns': team1_data['Touchdowns'].sum(),
            'Tackles': team1_data['Tackles'].sum(),
            'Sacks': team1_data['Sacks'].sum(),
            'Interceptions': team1_data['Interceptions'].sum(),
            'Games Played': team1_data['Games Played'].sum(),
            'Players': len(team1_data)
        }
        
        team2_stats = {
            'Total Yards': team2_data[['Passing Yards', 'Rushing Yards', 'Receiving Yards']].sum().sum(),
            'Passing Yards': team2_data['Passing Yards'].sum(),
            'Rushing Yards': team2_data['Rushing Yards'].sum(),
            'Receiving Yards': team2_data['Receiving Yards'].sum(),
            'Touchdowns': team2_data['Touchdowns'].sum(),
            'Tackles': team2_data['Tackles'].sum(),
            'Sacks': team2_data['Sacks'].sum(),
            'Interceptions': team2_data['Interceptions'].sum(),
            'Games Played': team2_data['Games Played'].sum(),
            'Players': len(team2_data)
        }
        
        # Calculate per-game averages
        team1_games = team1_stats['Games Played']
        team2_games = team2_stats['Games Played']
        
        team1_per_game = {
            'Yards per Game': team1_stats['Total Yards'] / team1_games if team1_games > 0 else 0,
            'Touchdowns per Game': team1_stats['Touchdowns'] / team1_games if team1_games > 0 else 0,
            'Tackles per Game': team1_stats['Tackles'] / team1_games if team1_games > 0 else 0,
            'Sacks per Game': team1_stats['Sacks'] / team1_games if team1_games > 0 else 0
        }
        
        team2_per_game = {
            'Yards per Game': team2_stats['Total Yards'] / team2_games if team2_games > 0 else 0,
            'Touchdowns per Game': team2_stats['Touchdowns'] / team2_games if team2_games > 0 else 0,
            'Tackles per Game': team2_stats['Tackles'] / team2_games if team2_games > 0 else 0,
            'Sacks per Game': team2_stats['Sacks'] / team2_games if team2_games > 0 else 0
        }
        
        # Display team comparison metrics
        st.subheader("📊 Team Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"{team1} Total Yards", f"{int(team1_stats['Total Yards']):,}")
            st.metric(f"{team2} Total Yards", f"{int(team2_stats['Total Yards']):,}")
        
        with col2:
            st.metric(f"{team1} Touchdowns", int(team1_stats['Touchdowns']))
            st.metric(f"{team2} Touchdowns", int(team2_stats['Touchdowns']))
        
        with col3:
            st.metric(f"{team1} Tackles", int(team1_stats['Tackles']))
            st.metric(f"{team2} Tackles", int(team2_stats['Tackles']))
        
        with col4:
            st.metric(f"{team1} Sacks", int(team1_stats['Sacks']))
            st.metric(f"{team2} Sacks", int(team2_stats['Sacks']))
        
        # Create comprehensive comparison charts
        comparison_tabs = st.tabs(["Total Stats", "Per Game Stats", "Offensive Breakdown", "Defensive Breakdown"])
        
        with comparison_tabs[0]:
            # Total stats comparison
            categories = ['Total Yards', 'Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns', 'Tackles', 'Sacks', 'Interceptions']
            team1_values = [team1_stats[cat] for cat in categories]
            team2_values = [team2_stats[cat] for cat in categories]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name=team1, x=categories, y=team1_values, marker_color='rgb(55, 83, 109)'))
            fig.add_trace(go.Bar(name=team2, x=categories, y=team2_values, marker_color='rgb(26, 118, 255)'))
            
            fig.update_layout(
                title=f"Total Statistics Comparison: {team1} vs {team2}",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with comparison_tabs[1]:
            # Per game stats comparison
            per_game_categories = ['Yards per Game', 'Touchdowns per Game', 'Tackles per Game', 'Sacks per Game']
            team1_per_game_values = [team1_per_game[cat] for cat in per_game_categories]
            team2_per_game_values = [team2_per_game[cat] for cat in per_game_categories]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name=team1, x=per_game_categories, y=team1_per_game_values, marker_color='rgb(55, 83, 109)'))
            fig.add_trace(go.Bar(name=team2, x=per_game_categories, y=team2_per_game_values, marker_color='rgb(26, 118, 255)'))
            
            fig.update_layout(
                title=f"Per Game Statistics Comparison: {team1} vs {team2}",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with comparison_tabs[2]:
            # Offensive breakdown
            offensive_categories = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns']
            team1_offensive = [team1_stats[cat] for cat in offensive_categories]
            team2_offensive = [team2_stats[cat] for cat in offensive_categories]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name=team1, x=offensive_categories, y=team1_offensive, marker_color='rgb(55, 83, 109)'))
            fig.add_trace(go.Bar(name=team2, x=offensive_categories, y=team2_offensive, marker_color='rgb(26, 118, 255)'))
            
            fig.update_layout(
                title=f"Offensive Statistics Comparison: {team1} vs {team2}",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with comparison_tabs[3]:
            # Defensive breakdown
            defensive_categories = ['Tackles', 'Sacks', 'Interceptions']
            team1_defensive = [team1_stats[cat] for cat in defensive_categories]
            team2_defensive = [team2_stats[cat] for cat in defensive_categories]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name=team1, x=defensive_categories, y=team1_defensive, marker_color='rgb(55, 83, 109)'))
            fig.add_trace(go.Bar(name=team2, x=defensive_categories, y=team2_defensive, marker_color='rgb(26, 118, 255)'))
            
            fig.update_layout(
                title=f"Defensive Statistics Comparison: {team1} vs {team2}",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Team roster comparison
        st.subheader("👥 Team Roster Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{team1} Roster ({len(team1_data)} players)**")
            team1_roster = team1_data[['Player Name', 'Position', 'Games Played', 'Touchdowns']].sort_values('Touchdowns', ascending=False)
            st.dataframe(team1_roster, use_container_width=True)
        
        with col2:
            st.write(f"**{team2} Roster ({len(team2_data)} players)**")
            team2_roster = team2_data[['Player Name', 'Position', 'Games Played', 'Touchdowns']].sort_values('Touchdowns', ascending=False)
            st.dataframe(team2_roster, use_container_width=True)

    # Individual Player Profile
    st.header("👤 Player Profile")
    
    # Allow multiple player selection for comparison
    selected_players_profile = st.multiselect(
        "Select Players for Profile Comparison (up to 5 players)",
        options=unique_players,
        default=[unique_players[0]] if unique_players else []
    )
    
    if selected_players_profile:
        # Create comparison layout
        if len(selected_players_profile) == 1:
            # Single player view (original layout)
            profile_data = filtered_data[filtered_data['Player Name'] == selected_players_profile[0]]
            
            if not profile_data.empty:
                player_info = profile_data.iloc[0]
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="player-card player-card-1">
                        <h3>{player_info['Player Name']}</h3>
                        <p><strong>Team:</strong> {player_info['Team']}</p>
                        <p><strong>Position:</strong> {player_info['Position']}</p>
                        <p><strong>Games Played:</strong> {player_info['Games Played']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Radar chart for player stats
                    radar_fig = create_player_profile(profile_data)
                    st.plotly_chart(radar_fig, use_container_width=True)
                
                with col3:
                    # Key stats
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>Key Statistics</h4>
                        <p><strong>Passing Yards:</strong> {int(player_info['Passing Yards']):,}</p>
                        <p><strong>Rushing Yards:</strong> {int(player_info['Rushing Yards']):,}</p>
                        <p><strong>Receiving Yards:</strong> {int(player_info['Receiving Yards']):,}</p>
                        <p><strong>Touchdowns:</strong> {int(player_info['Touchdowns'])}</p>
                        <p><strong>Tackles:</strong> {int(player_info['Tackles'])}</p>
                        <p><strong>Sacks:</strong> {int(player_info['Sacks'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            # Multiple player comparison view
            st.subheader("📊 Player Comparison")
            
            # Get data for all selected players
            comparison_data = filtered_data[filtered_data['Player Name'].isin(selected_players_profile)]
            
            if not comparison_data.empty:
                # Create comparison radar chart
                comparison_radar_fig = create_multi_player_profile(comparison_data)
                st.plotly_chart(comparison_radar_fig, use_container_width=True)
                
                # Create comparison table
                st.subheader("📋 Statistical Comparison")
                
                # Prepare comparison table
                comparison_table = comparison_data[['Player Name', 'Team', 'Position', 'Games Played', 
                                                 'Passing Yards', 'Rushing Yards', 'Receiving Yards', 
                                                 'Touchdowns', 'Tackles', 'Sacks']].copy()
                
                # Format numbers for better display
                for col in ['Passing Yards', 'Rushing Yards', 'Receiving Yards']:
                    comparison_table[col] = comparison_table[col].apply(lambda x: f"{int(x):,}")
                
                st.dataframe(comparison_table, use_container_width=True)
                
                # Create bar chart comparison for key stats
                st.subheader("📈 Performance Comparison")
                
                # Select stat to compare
                stat_options = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns', 'Tackles', 'Sacks']
                selected_stat = st.selectbox("Select Statistic to Compare", options=stat_options)
                
                if selected_stat:
                    comparison_chart = create_stat_comparison_chart(comparison_data, selected_stat)
                    st.plotly_chart(comparison_chart, use_container_width=True)
                
                # Individual player cards
                st.subheader("👤 Individual Player Details")
                
                # Create columns for player cards
                num_players = len(selected_players_profile)
                cols = st.columns(min(num_players, 3))  # Max 3 columns
                
                for i, player_name in enumerate(selected_players_profile):
                    player_data = comparison_data[comparison_data['Player Name'] == player_name]
                    if not player_data.empty:
                        player_info = player_data.iloc[0]
                        col_idx = i % 3
                        
                        with cols[col_idx]:
                            card_class = f"player-card player-card-{i+1}"
                            st.markdown(f"""
                            <div class="{card_class}">
                                <h4>{player_info['Player Name']}</h4>
                                <p><strong>Team:</strong> {player_info['Team']}</p>
                                <p><strong>Position:</strong> {player_info['Position']}</p>
                                <p><strong>Games:</strong> {player_info['Games Played']}</p>
                                <p><strong>Passing:</strong> {int(player_info['Passing Yards']):,}</p>
                                <p><strong>Rushing:</strong> {int(player_info['Rushing Yards']):,}</p>
                                <p><strong>Receiving:</strong> {int(player_info['Receiving Yards']):,}</p>
                                <p><strong>TDs:</strong> {int(player_info['Touchdowns'])}</p>
                                <p><strong>Tackles:</strong> {int(player_info['Tackles'])}</p>
                                <p><strong>Sacks:</strong> {int(player_info['Sacks'])}</p>
                            </div>
                            """, unsafe_allow_html=True)

    # Top Performers Section
    st.header("🏆 Top Performers (2024 Season)")
    
    # Calculate additional statistics for top performers
    filtered_data['Total Yards'] = filtered_data['Passing Yards'] + filtered_data['Rushing Yards'] + filtered_data['Receiving Yards']
    filtered_data['Total Offensive Yards'] = filtered_data['Rushing Yards'] + filtered_data['Receiving Yards']
    filtered_data['Yards per Game'] = filtered_data['Total Yards'] / filtered_data['Games Played']
    filtered_data['Touchdowns per Game'] = filtered_data['Touchdowns'] / filtered_data['Games Played']
    filtered_data['Tackles per Game'] = filtered_data['Tackles'] / filtered_data['Games Played']
    filtered_data['Sacks per Game'] = filtered_data['Sacks'] / filtered_data['Games Played']
    
    # Create comprehensive top performers analysis
    top_performers_tabs = st.tabs([
        "Total Yards", "Passing Leaders", "Rushing Leaders", "Receiving Leaders",
        "Touchdown Leaders", "Tackle Leaders", "Sack Leaders", "Per Game Leaders"
    ])
    
    with top_performers_tabs[0]:
        # Top 15 by Total Yards
        top_total_yards = filtered_data.nlargest(15, 'Total Yards')
        
        if not top_total_yards.empty:
            fig = px.bar(
                top_total_yards,
                x='Total Yards',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Players by Total Yards (2024 Season)",
                labels={'Total Yards': 'Total Yards', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Total Yards Leaders")
            display_data = top_total_yards[['Player Name', 'Team', 'Position', 'Games Played', 'Total Yards', 'Touchdowns']].copy()
            display_data['Total Yards'] = display_data['Total Yards'].apply(lambda x: f"{int(x):,}")
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[1]:
        # Top 15 by Passing Yards
        top_passing = filtered_data.nlargest(15, 'Passing Yards')
        
        if not top_passing.empty:
            fig = px.bar(
                top_passing,
                x='Passing Yards',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Quarterbacks by Passing Yards (2024 Season)",
                labels={'Passing Yards': 'Passing Yards', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Passing Leaders")
            display_data = top_passing[['Player Name', 'Team', 'Position', 'Games Played', 'Passing Yards', 'Touchdowns']].copy()
            display_data['Passing Yards'] = display_data['Passing Yards'].apply(lambda x: f"{int(x):,}")
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[2]:
        # Top 15 by Rushing Yards
        top_rushing = filtered_data.nlargest(15, 'Rushing Yards')
        
        if not top_rushing.empty:
            fig = px.bar(
                top_rushing,
                x='Rushing Yards',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Running Backs by Rushing Yards (2024 Season)",
                labels={'Rushing Yards': 'Rushing Yards', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Rushing Leaders")
            display_data = top_rushing[['Player Name', 'Team', 'Position', 'Games Played', 'Rushing Yards', 'Touchdowns']].copy()
            display_data['Rushing Yards'] = display_data['Rushing Yards'].apply(lambda x: f"{int(x):,}")
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[3]:
        # Top 15 by Receiving Yards
        top_receiving = filtered_data.nlargest(15, 'Receiving Yards')
        
        if not top_receiving.empty:
            fig = px.bar(
                top_receiving,
                x='Receiving Yards',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Wide Receivers by Receiving Yards (2024 Season)",
                labels={'Receiving Yards': 'Receiving Yards', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Receiving Leaders")
            display_data = top_receiving[['Player Name', 'Team', 'Position', 'Games Played', 'Receiving Yards', 'Touchdowns']].copy()
            display_data['Receiving Yards'] = display_data['Receiving Yards'].apply(lambda x: f"{int(x):,}")
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[4]:
        # Top 15 by Touchdowns
        top_touchdowns = filtered_data.nlargest(15, 'Touchdowns')
        
        if not top_touchdowns.empty:
            fig = px.bar(
                top_touchdowns,
                x='Touchdowns',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Players by Touchdowns (2024 Season)",
                labels={'Touchdowns': 'Touchdowns', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Touchdown Leaders")
            display_data = top_touchdowns[['Player Name', 'Team', 'Position', 'Games Played', 'Touchdowns', 'Total Yards']].copy()
            display_data['Total Yards'] = display_data['Total Yards'].apply(lambda x: f"{int(x):,}")
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[5]:
        # Top 15 by Tackles
        top_tackles = filtered_data.nlargest(15, 'Tackles')
        
        if not top_tackles.empty:
            fig = px.bar(
                top_tackles,
                x='Tackles',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Defensive Players by Tackles (2024 Season)",
                labels={'Tackles': 'Tackles', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Tackle Leaders")
            display_data = top_tackles[['Player Name', 'Team', 'Position', 'Games Played', 'Tackles', 'Sacks']].copy()
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[6]:
        # Top 15 by Sacks
        top_sacks = filtered_data.nlargest(15, 'Sacks')
        
        if not top_sacks.empty:
            fig = px.bar(
                top_sacks,
                x='Sacks',
                y='Player Name',
                color='Team',
                orientation='h',
                title="Top 15 Defensive Players by Sacks (2024 Season)",
                labels={'Sacks': 'Sacks', 'Player Name': 'Player'},
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Top 15 Sack Leaders")
            display_data = top_sacks[['Player Name', 'Team', 'Position', 'Games Played', 'Sacks', 'Tackles']].copy()
            st.dataframe(display_data, use_container_width=True)
    
    with top_performers_tabs[7]:
        # Per Game Leaders
        st.subheader("📊 Per Game Performance Leaders")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Yards per Game Leaders
            top_yards_per_game = filtered_data[filtered_data['Yards per Game'].notna()].nlargest(10, 'Yards per Game')
            
            if not top_yards_per_game.empty:
                fig = px.bar(
                    top_yards_per_game,
                    x='Yards per Game',
                    y='Player Name',
                    color='Team',
                    orientation='h',
                    title="Top 10 Players by Yards per Game",
                    labels={'Yards per Game': 'Yards per Game', 'Player Name': 'Player'},
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#fafafa'),
                    xaxis=dict(gridcolor='#464646'),
                    yaxis=dict(gridcolor='#464646')
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Touchdowns per Game Leaders
            top_tds_per_game = filtered_data[filtered_data['Touchdowns per Game'].notna()].nlargest(10, 'Touchdowns per Game')
            
            if not top_tds_per_game.empty:
                fig = px.bar(
                    top_tds_per_game,
                    x='Touchdowns per Game',
                    y='Player Name',
                    color='Team',
                    orientation='h',
                    title="Top 10 Players by Touchdowns per Game",
                    labels={'Touchdowns per Game': 'Touchdowns per Game', 'Player Name': 'Player'},
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#fafafa'),
                    xaxis=dict(gridcolor='#464646'),
                    yaxis=dict(gridcolor='#464646')
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Per game stats table
        st.subheader("📋 Per Game Statistics Leaders")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top 10 Yards per Game**")
            yards_per_game_data = filtered_data[filtered_data['Yards per Game'].notna()].nlargest(10, 'Yards per Game')[['Player Name', 'Team', 'Position', 'Games Played', 'Yards per Game']].copy()
            yards_per_game_data['Yards per Game'] = yards_per_game_data['Yards per Game'].apply(lambda x: f"{x:.1f}")
            st.dataframe(yards_per_game_data, use_container_width=True)
        
        with col2:
            st.write("**Top 10 Touchdowns per Game**")
            tds_per_game_data = filtered_data[filtered_data['Touchdowns per Game'].notna()].nlargest(10, 'Touchdowns per Game')[['Player Name', 'Team', 'Position', 'Games Played', 'Touchdowns per Game']].copy()
            tds_per_game_data['Touchdowns per Game'] = tds_per_game_data['Touchdowns per Game'].apply(lambda x: f"{x:.2f}")
            st.dataframe(tds_per_game_data, use_container_width=True)

    # Download filtered data
    st.header("📥 Download Data")
    
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name=f"cjfl_data_{'_'.join(map(str, selected_seasons))}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("*Data source: CJFL Statistics (2024 Season)*") 