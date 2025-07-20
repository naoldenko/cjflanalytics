#!/usr/bin/env python3
"""
CJFL Statistics Display Script
Shows accurate Canadian Junior Football League statistics
"""

import pandas as pd
import numpy as np

def load_cjfl_data():
    """Load CJFL statistics data"""
    try:
        data = pd.read_csv('data/cjfl_stats.csv')
        return data
    except FileNotFoundError:
        print("Error: CJFL stats file not found!")
        return None

def display_league_overview(data):
    """Display league overview statistics"""
    print("🏈 CJFL LEAGUE OVERVIEW")
    print("=" * 50)
    
    total_players = len(data['Player Name'].unique())
    total_teams = len(data['Team'].unique())
    total_seasons = len(data['Season'].unique())
    
    print(f"Total Players: {total_players}")
    print(f"Total Teams: {total_teams}")
    seasons_str = ', '.join(map(str, sorted(data['Season'].unique())))
    print(f"Seasons: {seasons_str}")
    print(f"Total Games Played: {data['Games Played'].sum():,}")
    print()

def display_team_stats(data):
    """Display team statistics"""
    print("🏆 TEAM STATISTICS")
    print("=" * 50)
    
    team_stats = data.groupby('Team').agg({
        'Player Name': 'count',
        'Passing Yards': 'sum',
        'Rushing Yards': 'sum',
        'Receiving Yards': 'sum',
        'Touchdowns': 'sum',
        'Tackles': 'sum',
        'Sacks': 'sum',
        'Interceptions': 'sum'
    }).round(0)
    
    team_stats.columns = ['Players', 'Pass Yds', 'Rush Yds', 'Rec Yds', 'TDs', 'Tackles', 'Sacks', 'INTs']
    team_stats['Total Yards'] = team_stats['Pass Yds'] + team_stats['Rush Yds'] + team_stats['Rec Yds']
    
    print(team_stats.sort_values('Total Yards', ascending=False))
    print()

def display_top_players(data, stat_column, top_n=10):
    """Display top players by specific statistic"""
    print(f"🏅 TOP {top_n} PLAYERS BY {stat_column.upper()}")
    print("=" * 50)
    
    top_players = data.nlargest(top_n, stat_column)[['Player Name', 'Team', 'Position', stat_column, 'Season']]
    
    for idx, row in top_players.iterrows():
        print(f"{row['Player Name']:<20} {row['Team']:<20} {row['Position']:<3} {row[stat_column]:>8,} ({row['Season']})")
    print()

def display_position_breakdown(data):
    """Display statistics by position"""
    print("📊 POSITION BREAKDOWN")
    print("=" * 50)
    
    pos_stats = data.groupby('Position').agg({
        'Player Name': 'count',
        'Passing Yards': 'sum',
        'Rushing Yards': 'sum',
        'Receiving Yards': 'sum',
        'Touchdowns': 'sum',
        'Tackles': 'sum',
        'Sacks': 'sum',
        'Interceptions': 'sum'
    }).round(0)
    
    pos_stats.columns = ['Players', 'Pass Yds', 'Rush Yds', 'Rec Yds', 'TDs', 'Tackles', 'Sacks', 'INTs']
    print(pos_stats)
    print()

def display_season_trends(data):
    """Display season-by-season trends"""
    print("📈 SEASON TRENDS")
    print("=" * 50)
    
    season_stats = data.groupby('Season').agg({
        'Player Name': 'count',
        'Passing Yards': 'sum',
        'Rushing Yards': 'sum',
        'Receiving Yards': 'sum',
        'Touchdowns': 'sum',
        'Tackles': 'sum',
        'Sacks': 'sum',
        'Interceptions': 'sum'
    }).round(0)
    
    season_stats.columns = ['Players', 'Pass Yds', 'Rush Yds', 'Rec Yds', 'TDs', 'Tackles', 'Sacks', 'INTs']
    season_stats['Total Yards'] = season_stats['Pass Yds'] + season_stats['Rush Yds'] + season_stats['Rec Yds']
    
    print(season_stats)
    print()

def display_player_search(data, search_term):
    """Search and display specific player statistics"""
    print(f"🔍 PLAYER SEARCH: '{search_term}'")
    print("=" * 50)
    
    matching_players = data[data['Player Name'].str.contains(search_term, case=False, na=False)]
    
    if matching_players.empty:
        print("No players found matching your search.")
        return
    
    for idx, player in matching_players.iterrows():
        print(f"\nPlayer: {player['Player Name']}")
        print(f"Team: {player['Team']}")
        print(f"Position: {player['Position']}")
        print(f"Season: {player['Season']}")
        print(f"Games: {player['Games Played']}")
        print(f"Passing Yards: {player['Passing Yards']:,}")
        print(f"Rushing Yards: {player['Rushing Yards']:,}")
        print(f"Receiving Yards: {player['Receiving Yards']:,}")
        print(f"Touchdowns: {player['Touchdowns']}")
        print(f"Tackles: {player['Tackles']}")
        print(f"Sacks: {player['Sacks']}")
        print(f"Interceptions: {player['Interceptions']}")
        print("-" * 30)

def main():
    """Main function to display CJFL statistics"""
    print("🏈 CANADIAN JUNIOR FOOTBALL LEAGUE STATISTICS")
    print("=" * 60)
    print()
    
    # Load data
    data = load_cjfl_data()
    if data is None:
        return
    
    # Display various statistics
    display_league_overview(data)
    display_team_stats(data)
    display_position_breakdown(data)
    display_season_trends(data)
    
    # Display top players by different categories
    display_top_players(data, 'Passing Yards')
    display_top_players(data, 'Rushing Yards')
    display_top_players(data, 'Receiving Yards')
    display_top_players(data, 'Touchdowns')
    display_top_players(data, 'Tackles')
    display_top_players(data, 'Sacks')
    display_top_players(data, 'Interceptions')
    
    # Interactive player search
    print("🔍 PLAYER SEARCH")
    print("=" * 50)
    search_term = input("Enter player name to search (or press Enter to skip): ").strip()
    
    if search_term:
        display_player_search(data, search_term)
    
    print("\n" + "=" * 60)
    print("📊 Statistics generated from CJFL data")
    print("Data includes multiple teams and seasons for comprehensive analysis")

if __name__ == "__main__":
    main() 