#!/usr/bin/env python3
"""
CJFL Data Collection Progress Dashboard
Shows progress of real data collection and works with partial data
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def load_progress_data():
    """Load progress data from JSON file"""
    progress_file = "data/collection_progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return None

def load_cjfl_data():
    """Load CJFL data (real or partial)"""
    try:
        data = pd.read_csv('data/cjfl_stats.csv')
        return data
    except FileNotFoundError:
        return None

def create_progress_dashboard():
    """Create the main progress dashboard"""
    st.set_page_config(
        page_title="CJFL Data Collection Progress",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stApp {
        background-color: #0e1117;
    }
    .progress-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #464646;
        margin: 0.5rem 0;
    }
    .status-completed { color: #00ff00; }
    .status-in-progress { color: #ffff00; }
    .status-not-started { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 CJFL Data Collection Progress Dashboard")
    st.markdown("**Track the progress of collecting real CJFL statistics**")
    
    # Load data
    progress_data = load_progress_data()
    cjfl_data = load_cjfl_data()
    
    if not progress_data:
        st.error("No progress data found. Run the data collection plan first.")
        return
    
    # Progress Overview
    col1, col2, col3, col4 = st.columns(4)
    
    total_teams = len(progress_data.get("teams", {}))
    completed_teams = sum(1 for team in progress_data["teams"].values() if team["status"] == "completed")
    in_progress_teams = sum(1 for team in progress_data["teams"].values() if team["status"] == "in_progress")
    not_started_teams = total_teams - completed_teams - in_progress_teams
    
    with col1:
        st.metric("Total Teams", total_teams)
    
    with col2:
        st.metric("Completed", completed_teams)
    
    with col3:
        st.metric("In Progress", in_progress_teams)
    
    with col4:
        st.metric("Total Players", progress_data.get("total_players_collected", 0))
    
    # Progress Chart
    st.header("📈 Collection Progress")
    
    progress_df = pd.DataFrame([
        {"Status": "Completed", "Count": completed_teams},
        {"Status": "In Progress", "Count": in_progress_teams},
        {"Status": "Not Started", "Count": not_started_teams}
    ])
    
    fig = px.pie(
        progress_df, 
        values="Count", 
        names="Status",
        title="Team Collection Status",
        color_discrete_map={
            "Completed": "#00ff00",
            "In Progress": "#ffff00", 
            "Not Started": "#ff0000"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Team Status Table
    st.header("🏈 Team Collection Status")
    
    if progress_data.get("teams"):
        team_data = []
        for team_name, team_info in progress_data["teams"].items():
            team_data.append({
                "Team": team_name,
                "Status": team_info["status"],
                "Players Collected": team_info.get("players_collected", 0),
                "Last Updated": team_info.get("last_updated", "Never"),
                "Notes": team_info.get("notes", "")
            })
        
        team_df = pd.DataFrame(team_data)
        
        # Color code the status
        def color_status(val):
            if val == "completed":
                return "background-color: #00ff00; color: black"
            elif val == "in_progress":
                return "background-color: #ffff00; color: black"
            else:
                return "background-color: #ff0000; color: white"
        
        styled_df = team_df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)
    
    # Real Data Analysis (if available)
    if cjfl_data is not None:
        st.header("📊 Real Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Data Overview")
            st.write(f"**Total Players:** {len(cjfl_data)}")
            st.write(f"**Total Teams:** {len(cjfl_data['Team'].unique())}")
            st.write(f"**Positions:** {', '.join(sorted(cjfl_data['Position'].unique()))}")
        
        with col2:
            st.subheader("Top Teams by Players")
            team_counts = cjfl_data['Team'].value_counts()
            fig = px.bar(
                x=team_counts.values,
                y=team_counts.index,
                orientation='h',
                title="Players per Team"
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fafafa'),
                xaxis=dict(gridcolor='#464646'),
                yaxis=dict(gridcolor='#464646')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top Players by Category
        st.subheader("🏆 Top Players (Real Data)")
        
        categories = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns', 'Tackles']
        
        for category in categories:
            if category in cjfl_data.columns:
                top_players = cjfl_data.nlargest(5, category)[['Player Name', 'Team', 'Position', category]]
                st.write(f"**{category}:**")
                for _, player in top_players.iterrows():
                    st.write(f"- {player['Player Name']} ({player['Team']}, {player['Position']}): {player[category]:,}")
                st.write("---")
    
    # Data Quality Metrics
    st.header("🔍 Data Quality Metrics")
    
    if cjfl_data is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Completeness
            total_cells = len(cjfl_data) * len(cjfl_data.columns)
            non_null_cells = cjfl_data.count().sum()
            completeness = (non_null_cells / total_cells) * 100
            st.metric("Data Completeness", f"{completeness:.1f}%")
        
        with col2:
            # Teams with data
            teams_with_data = len(cjfl_data['Team'].unique())
            st.metric("Teams with Data", teams_with_data)
        
        with col3:
            # Average players per team
            avg_players = len(cjfl_data) / len(cjfl_data['Team'].unique())
            st.metric("Avg Players/Team", f"{avg_players:.1f}")
    
    # Next Steps
    st.header("🎯 Next Steps")
    
    if progress_data.get("teams"):
        not_started = [team for team, info in progress_data["teams"].items() if info["status"] == "not_started"]
        in_progress = [team for team, info in progress_data["teams"].items() if info["status"] == "in_progress"]
        
        if not_started:
            st.write("**Teams to Start:**")
            for team in not_started[:3]:  # Show next 3
                st.write(f"- {team}")
        
        if in_progress:
            st.write("**Teams in Progress:**")
            for team in in_progress:
                st.write(f"- {team}")
    
    # Data Collection Tips
    st.header("💡 Data Collection Tips")
    
    tips = [
        "Start with Priority 1 teams (Calgary Colts, Edmonton Wildcats, Saskatoon Hilltops)",
        "Check team websites for roster pages and statistics sections",
        "Use social media to find game reports and player highlights",
        "Contact teams directly via email for official statistics",
        "Focus on 2024 season data only",
        "Include all players, not just starters",
        "Use the template file for consistent data entry"
    ]
    
    for tip in tips:
        st.write(f"• {tip}")

def main():
    """Main function"""
    create_progress_dashboard()

if __name__ == "__main__":
    main() 