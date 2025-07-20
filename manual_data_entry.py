#!/usr/bin/env python3
"""
Manual Data Entry Tool for CJFL Statistics
Helps enter player data as it's collected from teams
"""

import pandas as pd
import json
import os
from datetime import datetime

class ManualDataEntry:
    def __init__(self):
        self.data_file = "data/cjfl_stats.csv"
        self.template_file = "data/cjfl_real_data_template.csv"
        self.progress_file = "data/collection_progress.json"
        
    def add_player(self, team_name):
        """Add a new player to the dataset"""
        print(f"\n📝 ADDING PLAYER FOR {team_name}")
        print("=" * 40)
        
        # Get player information
        player_name = input("Player Name (Full Name): ").strip()
        if not player_name:
            print("❌ Player name is required")
            return
        
        # Position selection
        positions = ["QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "K", "P"]
        print("\nPositions available:")
        for i, pos in enumerate(positions, 1):
            print(f"{i}. {pos}")
        
        try:
            pos_choice = int(input(f"\nSelect position (1-{len(positions)}): "))
            position = positions[pos_choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid position selection")
            return
        
        # Get statistics
        print(f"\n📊 Enter statistics for {player_name} ({position}):")
        
        try:
            games_played = int(input("Games Played (2024 season): ") or "0")
            passing_yards = int(input("Passing Yards (QBs only): ") or "0")
            rushing_yards = int(input("Rushing Yards: ") or "0")
            receiving_yards = int(input("Receiving Yards: ") or "0")
            touchdowns = int(input("Touchdowns: ") or "0")
            tackles = int(input("Tackles (defensive players): ") or "0")
            sacks = int(input("Sacks (DL, LB): ") or "0")
            interceptions = int(input("Interceptions (DB, LB): ") or "0")
        except ValueError:
            print("❌ Invalid number entered")
            return
        
        # Create player data
        player_data = {
            "Player Name": player_name,
            "Team": team_name,
            "Position": position,
            "Season": 2024,
            "Games Played": games_played,
            "Passing Yards": passing_yards,
            "Rushing Yards": rushing_yards,
            "Receiving Yards": receiving_yards,
            "Touchdowns": touchdowns,
            "Tackles": tackles,
            "Sacks": sacks,
            "Interceptions": interceptions
        }
        
        # Add to dataset
        self.add_player_to_dataset(player_data)
        
        # Update progress
        self.update_progress(team_name, 1)
        
        print(f"✅ Added {player_name} to {team_name} dataset")
    
    def add_player_to_dataset(self, player_data):
        """Add player data to the CSV file"""
        try:
            # Load existing data
            if os.path.exists(self.data_file):
                df = pd.read_csv(self.data_file)
            else:
                # Use template structure
                df = pd.read_csv(self.template_file)
                df = df[df['Team'] != player_data['Team']]  # Remove template entries for this team
            
            # Add new player data
            new_row = pd.DataFrame([player_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save updated data
            df.to_csv(self.data_file, index=False)
            
        except Exception as e:
            print(f"❌ Error adding player data: {str(e)}")
    
    def update_progress(self, team_name, players_added):
        """Update progress tracking"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                progress = json.load(f)
        else:
            progress = {
                "start_date": datetime.now().isoformat(),
                "teams": {},
                "total_players_collected": 0,
                "total_teams_completed": 0,
                "last_updated": datetime.now().isoformat()
            }
        
        if team_name not in progress["teams"]:
            progress["teams"][team_name] = {
                "status": "in_progress",
                "players_collected": 0,
                "data_sources_checked": [],
                "notes": "",
                "last_updated": datetime.now().isoformat()
            }
        
        progress["teams"][team_name]["players_collected"] += players_added
        progress["teams"][team_name]["last_updated"] = datetime.now().isoformat()
        progress["total_players_collected"] += players_added
        progress["last_updated"] = datetime.now().isoformat()
        
        os.makedirs("data", exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def view_current_data(self, team_name=None):
        """View current data for a team or all teams"""
        if not os.path.exists(self.data_file):
            print("❌ No data file found")
            return
        
        df = pd.read_csv(self.data_file)
        
        if team_name:
            df = df[df['Team'] == team_name]
            if df.empty:
                print(f"❌ No data found for {team_name}")
                return
            print(f"\n📊 CURRENT DATA FOR {team_name.upper()}:")
        else:
            print(f"\n📊 CURRENT DATA FOR ALL TEAMS:")
        
        print("=" * 50)
        
        # Group by team
        for team in df['Team'].unique():
            team_data = df[df['Team'] == team]
            print(f"\n🏈 {team}:")
            print(f"   Players: {len(team_data)}")
            print(f"   Positions: {', '.join(team_data['Position'].unique())}")
            
            # Show top players by touchdowns
            if not team_data.empty and 'Touchdowns' in team_data.columns:
                top_players = team_data.nlargest(3, 'Touchdowns')
                print("   Top Scorers:")
                for _, player in top_players.iterrows():
                    print(f"     {player['Player Name']} ({player['Position']}): {player['Touchdowns']} TDs")
    
    def mark_team_complete(self, team_name):
        """Mark a team as complete in progress tracking"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                progress = json.load(f)
        else:
            progress = {
                "start_date": datetime.now().isoformat(),
                "teams": {},
                "total_players_collected": 0,
                "total_teams_completed": 0,
                "last_updated": datetime.now().isoformat()
            }
        
        if team_name not in progress["teams"]:
            progress["teams"][team_name] = {
                "status": "completed",
                "players_collected": 0,
                "data_sources_checked": [],
                "notes": "Marked complete manually",
                "last_updated": datetime.now().isoformat()
            }
        else:
            progress["teams"][team_name]["status"] = "completed"
            progress["teams"][team_name]["notes"] = "Marked complete manually"
            progress["teams"][team_name]["last_updated"] = datetime.now().isoformat()
        
        progress["total_teams_completed"] += 1
        progress["last_updated"] = datetime.now().isoformat()
        
        os.makedirs("data", exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
        
        print(f"✅ Marked {team_name} as complete")
    
    def show_menu(self):
        """Show the main menu"""
        print("\n🏈 CJFL MANUAL DATA ENTRY TOOL")
        print("=" * 40)
        print("1. Add player data")
        print("2. View current data")
        print("3. Mark team complete")
        print("4. Show progress summary")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        return choice

def main():
    """Main function"""
    entry_tool = ManualDataEntry()
    
    while True:
        choice = entry_tool.show_menu()
        
        if choice == "1":
            team_name = input("Enter team name: ").strip()
            if team_name:
                entry_tool.add_player(team_name)
            else:
                print("❌ Team name is required")
        
        elif choice == "2":
            team_name = input("Enter team name (or press Enter for all teams): ").strip()
            entry_tool.view_current_data(team_name if team_name else None)
        
        elif choice == "3":
            team_name = input("Enter team name to mark complete: ").strip()
            if team_name:
                entry_tool.mark_team_complete(team_name)
            else:
                print("❌ Team name is required")
        
        elif choice == "4":
            print("\n📊 PROGRESS SUMMARY:")
            print("=" * 30)
            if os.path.exists(entry_tool.progress_file):
                with open(entry_tool.progress_file, 'r') as f:
                    progress = json.load(f)
                
                total_teams = len(progress["teams"])
                completed = sum(1 for team in progress["teams"].values() if team["status"] == "completed")
                in_progress = sum(1 for team in progress["teams"].values() if team["status"] == "in_progress")
                not_started = total_teams - completed - in_progress
                
                print(f"Total Teams: {total_teams}")
                print(f"Completed: {completed}")
                print(f"In Progress: {in_progress}")
                print(f"Not Started: {not_started}")
                print(f"Total Players: {progress.get('total_players_collected', 0)}")
            else:
                print("No progress data found")
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 