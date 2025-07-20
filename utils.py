import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional

def generate_cjfl_data() -> pd.DataFrame:
    """
    Generate realistic CJFL player statistics data for 2022-2024 seasons.
    This simulates data that would normally be scraped from CJFL official sources.
    """
    # CJFL teams (real teams from the league)
    teams = [
        "Calgary Colts", "Edmonton Wildcats", "Saskatoon Hilltops", "Regina Thunder",
        "Winnipeg Rifles", "Vancouver Island Raiders", "Okanagan Sun", "Langley Rams",
        "Westshore Rebels", "Valley Huskers", "Kamloops Broncos", "Prince George Kodiaks"
    ]
    
    # Player positions
    positions = ["QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "K", "P"]
    
    # Generate player names
    first_names = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
        "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
        "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
        "George", "Timothy", "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob",
        "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
        "Brandon", "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander",
        "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam",
        "Nathan", "Henry", "Douglas", "Zachary", "Peter", "Kyle", "Walter", "Ethan",
        "Jeremy", "Harold", "Carl", "Keith", "Roger", "Gerald", "Christian", "Terry",
        "Sean", "Austin", "Arthur", "Noah", "Lawrence", "Jesse", "Joe", "Bryan",
        "Billy", "Jordan", "Albert", "Dylan", "Bruce", "Willie", "Gabriel", "Alan",
        "Juan", "Logan", "Wayne", "Roy", "Ralph", "Randy", "Eugene", "Vincent",
        "Russell", "Elijah", "Louis", "Bobby", "Philip", "Johnny"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
        "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
        "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
        "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
        "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox",
        "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett",
        "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders",
        "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
    ]
    
    # Generate data for 3 seasons
    data = []
    seasons = [2022, 2023, 2024]
    
    for season in seasons:
        # Generate 150-200 players per season
        num_players = np.random.randint(150, 201)
        
        for _ in range(num_players):
            player_name = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
            team = np.random.choice(teams)
            position = np.random.choice(positions)
            
            # Generate realistic stats based on position
            games_played = np.random.randint(8, 13)
            
            # Offensive stats
            if position in ["QB"]:
                passing_yards = np.random.randint(1500, 3500)
                rushing_yards = np.random.randint(100, 800)
                receiving_yards = 0
                touchdowns = np.random.randint(15, 35)
            elif position in ["RB"]:
                passing_yards = 0
                rushing_yards = np.random.randint(800, 2000)
                receiving_yards = np.random.randint(100, 500)
                touchdowns = np.random.randint(8, 20)
            elif position in ["WR", "TE"]:
                passing_yards = 0
                rushing_yards = np.random.randint(0, 200)
                receiving_yards = np.random.randint(400, 1200)
                touchdowns = np.random.randint(3, 15)
            else:
                passing_yards = 0
                rushing_yards = 0
                receiving_yards = 0
                touchdowns = 0
            
            # Defensive stats
            if position in ["DL", "LB", "DB"]:
                tackles = np.random.randint(20, 80)
                sacks = np.random.randint(0, 8) if position in ["DL", "LB"] else 0
                interceptions = np.random.randint(0, 5) if position in ["DB", "LB"] else 0
            else:
                tackles = 0
                sacks = 0
                interceptions = 0
            
            data.append({
                'Player Name': player_name,
                'Team': team,
                'Position': position,
                'Season': season,
                'Games Played': games_played,
                'Passing Yards': passing_yards,
                'Rushing Yards': rushing_yards,
                'Receiving Yards': receiving_yards,
                'Touchdowns': touchdowns,
                'Tackles': tackles,
                'Sacks': sacks,
                'Interceptions': interceptions
            })
    
    return pd.DataFrame(data)

def load_data() -> pd.DataFrame:
    """
    Load CJFL data. If no CSV file exists, generate simulated data.
    In a real implementation, this would load from a CSV file or database.
    """
    try:
        # Try to load from CSV file
        data = pd.read_csv('data/cjfl_stats.csv')
        return data
    except FileNotFoundError:
        # Generate simulated data if no file exists
        data = generate_cjfl_data()
        
        # Create data directory if it doesn't exist
        import os
        os.makedirs('data', exist_ok=True)
        
        # Save the generated data
        data.to_csv('data/cjfl_stats.csv', index=False)
        return data

def filter_data(data: pd.DataFrame, 
                seasons: List[int], 
                teams: List[str], 
                positions: List[str], 
                player_search: str) -> pd.DataFrame:
    """
    Filter the dataset based on user selections.
    """
    filtered = data.copy()
    
    # Filter by seasons
    if seasons:
        filtered = filtered[filtered['Season'].isin(seasons)]
    
    # Filter by teams
    if teams:
        filtered = filtered[filtered['Team'].isin(teams)]
    
    # Filter by positions
    if positions:
        filtered = filtered[filtered['Position'].isin(positions)]
    
    # Filter by player search
    if player_search:
        filtered = filtered[filtered['Player Name'].str.contains(player_search, case=False, na=False)]
    
    return filtered

def create_player_profile(player_data: pd.DataFrame) -> go.Figure:
    """
    Create a radar chart for player profile visualization.
    """
    if player_data.empty:
        return go.Figure()
    
    player_stats = player_data.iloc[0]
    
    # Normalize stats for radar chart (0-100 scale)
    max_values = {
        'Passing Yards': 3500,
        'Rushing Yards': 2000,
        'Receiving Yards': 1200,
        'Touchdowns': 35,
        'Tackles': 80,
        'Sacks': 8
    }
    
    categories = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns', 'Tackles', 'Sacks']
    values = []
    
    for category in categories:
        if category in max_values:
            normalized_value = min(100, (player_stats[category] / max_values[category]) * 100)
            values.append(normalized_value)
        else:
            values.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player_stats['Player Name'],
        line_color='rgb(32, 201, 151)',
        fillcolor='rgba(32, 201, 151, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title=f"Player Profile: {player_stats['Player Name']}",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa')
    )
    
    return fig

def create_team_comparison(data: pd.DataFrame, team1: str, team2: str) -> go.Figure:
    """
    Create a comparison chart between two teams.
    """
    team1_data = data[data['Team'] == team1]
    team2_data = data[data['Team'] == team2]
    
    # Calculate team statistics
    team1_stats = {
        'Total Yards': team1_data[['Passing Yards', 'Rushing Yards', 'Receiving Yards']].sum().sum(),
        'Touchdowns': team1_data['Touchdowns'].sum(),
        'Tackles': team1_data['Tackles'].sum(),
        'Sacks': team1_data['Sacks'].sum(),
        'Interceptions': team1_data['Interceptions'].sum()
    }
    
    team2_stats = {
        'Total Yards': team2_data[['Passing Yards', 'Rushing Yards', 'Receiving Yards']].sum().sum(),
        'Touchdowns': team2_data['Touchdowns'].sum(),
        'Tackles': team2_data['Tackles'].sum(),
        'Sacks': team2_data['Sacks'].sum(),
        'Interceptions': team2_data['Interceptions'].sum()
    }
    
    categories = list(team1_stats.keys())
    team1_values = list(team1_stats.values())
    team2_values = list(team2_stats.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=team1,
        x=categories,
        y=team1_values,
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Bar(
        name=team2,
        x=categories,
        y=team2_values,
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title=f"Team Comparison: {team1} vs {team2}",
        xaxis_title="Statistics",
        yaxis_title="Values",
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa'),
        xaxis=dict(gridcolor='#464646'),
        yaxis=dict(gridcolor='#464646')
    )
    
    return fig

def create_multi_player_profile(player_data: pd.DataFrame) -> go.Figure:
    """
    Create a radar chart for multiple player profile comparison.
    """
    if player_data.empty:
        return go.Figure()
    
    # Normalize stats for radar chart (0-100 scale)
    max_values = {
        'Passing Yards': 3500,
        'Rushing Yards': 2000,
        'Receiving Yards': 1200,
        'Touchdowns': 35,
        'Tackles': 80,
        'Sacks': 8
    }
    
    categories = ['Passing Yards', 'Rushing Yards', 'Receiving Yards', 'Touchdowns', 'Tackles', 'Sacks']
    
    fig = go.Figure()
    
    # Enhanced color palette for multiple players with better differentiation
    colors = [
        'rgb(255, 99, 132)',    # Red
        'rgb(54, 162, 235)',    # Blue
        'rgb(255, 205, 86)',    # Yellow
        'rgb(75, 192, 192)',    # Teal
        'rgb(153, 102, 255)',   # Purple
        'rgb(255, 159, 64)',    # Orange
        'rgb(199, 199, 199)',   # Gray
        'rgb(83, 102, 255)',    # Indigo
        'rgb(255, 99, 71)',     # Tomato
        'rgb(50, 205, 50)'      # Lime Green
    ]
    
    for idx, (_, player_stats) in enumerate(player_data.iterrows()):
        values = []
        
        for category in categories:
            if category in max_values:
                normalized_value = min(100, (player_stats[category] / max_values[category]) * 100)
                values.append(normalized_value)
            else:
                values.append(0)
        
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_stats['Player Name'],
            line_color=color,
            fillcolor=color.replace('rgb', 'rgba').replace(')', ', 0.3)'),
            opacity=0.8,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Multi-Player Profile Comparison",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#464646',
            borderwidth=1
        )
    )
    
    return fig

def create_stat_comparison_chart(player_data: pd.DataFrame, stat_name: str) -> go.Figure:
    """
    Create a bar chart comparing a specific statistic across multiple players.
    """
    if player_data.empty:
        return go.Figure()
    
    # Sort players by the selected stat
    sorted_data = player_data.sort_values(stat_name, ascending=True)
    
    fig = go.Figure()
    
    # Enhanced color palette for individual players
    colors = [
        'rgb(255, 99, 132)',    # Red
        'rgb(54, 162, 235)',    # Blue
        'rgb(255, 205, 86)',    # Yellow
        'rgb(75, 192, 192)',    # Teal
        'rgb(153, 102, 255)',   # Purple
        'rgb(255, 159, 64)',    # Orange
        'rgb(199, 199, 199)',   # Gray
        'rgb(83, 102, 255)',    # Indigo
        'rgb(255, 99, 71)',     # Tomato
        'rgb(50, 205, 50)'      # Lime Green
    ]
    
    # Color each player individually for better differentiation
    for idx, (_, player_stats) in enumerate(sorted_data.iterrows()):
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Bar(
            x=[player_stats['Player Name']],
            y=[player_stats[stat_name]],
            name=player_stats['Player Name'],
            marker_color=color,
            text=[f"{int(player_stats[stat_name]):,}" if stat_name in ['Passing Yards', 'Rushing Yards', 'Receiving Yards'] else str(int(player_stats[stat_name]))],
            textposition='auto',
            showlegend=True
        ))
    
    fig.update_layout(
        title=f"{stat_name} Comparison",
        xaxis_title="Players",
        yaxis_title=stat_name,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fafafa'),
        xaxis=dict(gridcolor='#464646'),
        yaxis=dict(gridcolor='#464646'),
        barmode='group',
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#464646',
            borderwidth=1
        )
    )
    
    return fig 