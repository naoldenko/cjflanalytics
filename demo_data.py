#!/usr/bin/env python3
"""
Demo script to showcase CJFL Analytics Dashboard data
"""

import pandas as pd
from utils import load_data

def main():
    print("🏈 CJFL Analytics Dashboard - Data Demo")
    print("=" * 50)
    
    # Load data
    data = load_data()
    
    print(f"📊 Dataset Overview:")
    print(f"   Total Records: {len(data):,}")
    print(f"   Seasons: {sorted(data['Season'].unique())}")
    print(f"   Teams: {len(data['Team'].unique())}")
    print(f"   Positions: {sorted(data['Position'].unique())}")
    print(f"   Unique Players: {data['Player Name'].nunique()}")
    
    print(f"\n🏆 Top Performers by Category:")
    
    # Top 5 by different stats
    categories = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns', 'Tackles', 'Sacks']
    
    for category in categories:
        top_players = data.nlargest(3, category)[['Player Name', 'Team', 'Position', category, 'Season']]
        print(f"\n   {category}:")
        for _, player in top_players.iterrows():
            print(f"     {player['Player Name']} ({player['Team']}, {player['Position']}) - {player[category]:,} ({player['Season']})")
    
    print(f"\n📈 Team Statistics:")
    team_stats = data.groupby('Team').agg({
        'Touchdowns': 'sum',
        'Passing Yards': 'sum',
        'Rushing Yards': 'sum',
        'Receiving Yards': 'sum',
        'Tackles': 'sum',
        'Sacks': 'sum'
    }).round(0)
    
    team_stats['Total Yards'] = team_stats['Passing Yards'] + team_stats['Rushing Yards'] + team_stats['Receiving Yards']
    
    # Show top 5 teams by total yards
    top_teams = team_stats.nlargest(5, 'Total Yards')
    for team, stats in top_teams.iterrows():
        print(f"   {team}: {stats['Total Yards']:,.0f} total yards, {stats['Touchdowns']:.0f} TDs")
    
    print(f"\n🎯 Position Breakdown:")
    pos_stats = data.groupby('Position').agg({
        'Player Name': 'count',
        'Touchdowns': 'sum',
        'Passing Yards': 'sum',
        'Rushing Yards': 'sum',
        'Receiving Yards': 'sum'
    }).round(0)
    
    for pos, stats in pos_stats.iterrows():
        total_yards = stats['Passing Yards'] + stats['Rushing Yards'] + stats['Receiving Yards']
        print(f"   {pos}: {stats['Player Name']} players, {total_yards:,.0f} total yards, {stats['Touchdowns']:.0f} TDs")
    
    print(f"\n📅 Season Trends:")
    season_stats = data.groupby('Season').agg({
        'Player Name': 'nunique',
        'Touchdowns': 'sum',
        'Passing Yards': 'sum',
        'Rushing Yards': 'sum',
        'Receiving Yards': 'sum'
    }).round(0)
    
    for season, stats in season_stats.iterrows():
        total_yards = stats['Passing Yards'] + stats['Rushing Yards'] + stats['Receiving Yards']
        print(f"   {season}: {stats['Player Name']} players, {total_yards:,.0f} total yards, {stats['Touchdowns']:.0f} TDs")
    
    print(f"\n🚀 Ready to explore!")
    print(f"   Run 'streamlit run app.py' to start the interactive dashboard")
    print(f"   Or run './run_dashboard.sh' for automatic setup")

if __name__ == "__main__":
    main() 