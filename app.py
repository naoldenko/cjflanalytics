import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils import load_data, filter_data, create_player_profile, create_team_comparison

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
st.markdown("**Canadian Junior Football League Player Statistics (2022-2024)**")

# Sidebar filters
st.sidebar.header("📊 Filters")

# Season filter
selected_seasons = st.sidebar.multiselect(
    "Select Seasons",
    options=sorted(data['Season'].unique()),
    default=sorted(data['Season'].unique())
)

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
    
    # Create tabs for different stat categories
    stat_tabs = st.tabs(["Passing Yards", "Rushing Yards", "Receiving Yards", "Touchdowns", "Tackles", "Sacks"])
    
    stat_columns = {
        "Passing Yards": "Passing Yards",
        "Rushing Yards": "Rushing Yards", 
        "Receiving Yards": "Receiving Yards",
        "Touchdowns": "Touchdowns",
        "Tackles": "Tackles",
        "Sacks": "Sacks"
    }
    
    for tab, (tab_name, column) in zip(stat_tabs, stat_columns.items()):
        with tab:
            top_players = filtered_data.nlargest(10, column)[['Player Name', 'Team', 'Position', column, 'Season']]
            
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

    # Stat Trends Over Years
    st.header("📈 Player Performance Trends")
    
    # Player selector for trends
    unique_players = sorted(filtered_data['Player Name'].unique())
    selected_player_trend = st.selectbox(
        "Select Player for Trend Analysis",
        options=unique_players,
        index=0 if unique_players else None
    )
    
    if selected_player_trend:
        player_trend_data = filtered_data[filtered_data['Player Name'] == selected_player_trend]
        
        if not player_trend_data.empty:
            # Create subplot for multiple stats
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            stats_to_plot = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns']
            positions = [(1,1), (1,2), (2,1), (2,2)]
            
            for stat, pos in zip(stats_to_plot, positions):
                fig.add_trace(
                    go.Scatter(
                        x=player_trend_data['Season'],
                        y=player_trend_data[stat],
                        mode='lines+markers',
                        name=stat,
                        line=dict(width=3)
                    ),
                    row=pos[0], col=pos[1]
                )
            
            fig.update_layout(
                title=f"Performance Trends for {selected_player_trend}",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                height=600
            )
            
            fig.update_xaxes(gridcolor='#464646')
            fig.update_yaxes(gridcolor='#464646')
            
            st.plotly_chart(fig, use_container_width=True)

    # Team vs Team Comparison
    st.header("🏆 Team Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        team1 = st.selectbox("Select Team 1", options=sorted(filtered_data['Team'].unique()))
    
    with col2:
        team2 = st.selectbox("Select Team 2", options=sorted(filtered_data['Team'].unique()), index=1 if len(filtered_data['Team'].unique()) > 1 else 0)
    
    if team1 and team2:
        comparison_fig = create_team_comparison(filtered_data, team1, team2)
        st.plotly_chart(comparison_fig, use_container_width=True)

    # Individual Player Profile
    st.header("👤 Player Profile")
    
    selected_player_profile = st.selectbox(
        "Select Player for Profile",
        options=unique_players,
        index=0 if unique_players else None
    )
    
    if selected_player_profile:
        profile_data = filtered_data[filtered_data['Player Name'] == selected_player_profile]
        
        if not profile_data.empty:
            # Player info card
            player_info = profile_data.iloc[0]
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="player-card">
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

    # Emerging Talent Section
    st.header("⭐ Emerging Talent (Under 21)")
    
    # Simulate age data for emerging talent
    emerging_data = filtered_data.copy()
    emerging_data['Age'] = np.random.randint(18, 22, size=len(emerging_data))
    emerging_talent = emerging_data[emerging_data['Age'] < 21]
    
    if not emerging_talent.empty:
        # Top emerging players by total yards
        emerging_talent['Total Yards'] = emerging_talent['Passing Yards'] + emerging_talent['Rushing Yards'] + emerging_talent['Receiving Yards']
        top_emerging = emerging_talent.nlargest(10, 'Total Yards')
        
        fig = px.bar(
            top_emerging,
            x='Total Yards',
            y='Player Name',
            color='Team',
            orientation='h',
            title="Top Emerging Talent by Total Yards",
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
    else:
        st.info("No emerging talent data available for the selected filters.")

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
st.markdown("*Data source: CJFL Statistics (Simulated for demonstration purposes)*") 