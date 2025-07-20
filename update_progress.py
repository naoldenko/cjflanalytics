#!/usr/bin/env python3
"""
CJFL Progress Update Script
Simple tool to update data collection progress
"""

import json
import os
from datetime import datetime

def load_progress():
    """Load current progress"""
    progress_file = "data/collection_progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return None

def save_progress(progress):
    """Save progress data"""
    os.makedirs("data", exist_ok=True)
    with open("data/collection_progress.json", 'w') as f:
        json.dump(progress, f, indent=2)

def update_team_status():
    """Update team collection status"""
    progress = load_progress()
    if not progress:
        print("❌ No progress data found. Run data_collection_plan.py first.")
        return
    
    print("🏈 CJFL PROGRESS UPDATE")
    print("=" * 40)
    
    # Show current teams
    print("\n📋 CURRENT TEAMS:")
    for i, team_name in enumerate(progress.get("teams", {}).keys(), 1):
        status = progress["teams"][team_name]["status"]
        players = progress["teams"][team_name].get("players_collected", 0)
        print(f"{i}. {team_name} - {status} ({players} players)")
    
    print(f"{len(progress.get('teams', {})) + 1}. Add new team")
    
    # Get user choice
    try:
        choice = int(input("\nSelect team to update (or 0 to exit): "))
        if choice == 0:
            return
        
        teams = list(progress.get("teams", {}).keys())
        
        if choice <= len(teams):
            team_name = teams[choice - 1]
            update_specific_team(progress, team_name)
        elif choice == len(teams) + 1:
            add_new_team(progress)
        else:
            print("❌ Invalid choice")
            
    except ValueError:
        print("❌ Please enter a valid number")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

def update_specific_team(progress, team_name):
    """Update status for a specific team"""
    print(f"\n🏈 UPDATING: {team_name}")
    print("=" * 40)
    
    print("Status options:")
    print("1. not_started")
    print("2. in_progress") 
    print("3. completed")
    print("4. no_data_available")
    
    try:
        status_choice = int(input("Select status: "))
        status_map = {
            1: "not_started",
            2: "in_progress",
            3: "completed", 
            4: "no_data_available"
        }
        
        if status_choice in status_map:
            new_status = status_map[status_choice]
            
            # Get player count
            try:
                player_count = int(input("Number of players collected (0 if none): "))
            except ValueError:
                player_count = 0
            
            # Get notes
            notes = input("Notes (optional): ")
            
            # Update progress
            if team_name not in progress["teams"]:
                progress["teams"][team_name] = {
                    "status": "not_started",
                    "players_collected": 0,
                    "data_sources_checked": [],
                    "notes": "",
                    "last_updated": datetime.now().isoformat()
                }
            
            progress["teams"][team_name]["status"] = new_status
            progress["teams"][team_name]["players_collected"] = player_count
            progress["teams"][team_name]["notes"] = notes
            progress["teams"][team_name]["last_updated"] = datetime.now().isoformat()
            
            # Update total players
            if new_status == "completed":
                progress["total_players_collected"] += player_count
            
            save_progress(progress)
            print(f"✅ Updated {team_name}: {new_status} ({player_count} players)")
            
        else:
            print("❌ Invalid status choice")
            
    except ValueError:
        print("❌ Please enter a valid number")

def add_new_team(progress):
    """Add a new team to track"""
    print("\n🏈 ADD NEW TEAM")
    print("=" * 40)
    
    team_name = input("Team name: ")
    website = input("Website URL: ")
    contact = input("Contact email: ")
    priority = int(input("Priority (1-3): "))
    
    if team_name not in progress["teams"]:
        progress["teams"][team_name] = {
            "status": "not_started",
            "players_collected": 0,
            "data_sources_checked": [],
            "notes": f"Website: {website}, Contact: {contact}, Priority: {priority}",
            "last_updated": datetime.now().isoformat()
        }
        
        save_progress(progress)
        print(f"✅ Added {team_name}")
    else:
        print(f"❌ {team_name} already exists")

def show_progress_summary():
    """Show current progress summary"""
    progress = load_progress()
    if not progress:
        print("❌ No progress data found")
        return
    
    print("\n📊 PROGRESS SUMMARY")
    print("=" * 40)
    
    total_teams = len(progress.get("teams", {}))
    completed = sum(1 for team in progress["teams"].values() if team["status"] == "completed")
    in_progress = sum(1 for team in progress["teams"].values() if team["status"] == "in_progress")
    not_started = sum(1 for team in progress["teams"].values() if team["status"] == "not_started")
    no_data = sum(1 for team in progress["teams"].values() if team["status"] == "no_data_available")
    
    print(f"Total Teams: {total_teams}")
    print(f"Completed: {completed}")
    print(f"In Progress: {in_progress}")
    print(f"Not Started: {not_started}")
    print(f"No Data Available: {no_data}")
    print(f"Total Players: {progress.get('total_players_collected', 0)}")
    
    if progress.get("start_date"):
        from datetime import datetime
        start_date = datetime.fromisoformat(progress["start_date"])
        days_elapsed = (datetime.now() - start_date).days
        print(f"Days Elapsed: {days_elapsed}")

def main():
    """Main function"""
    print("🏈 CJFL PROGRESS UPDATE TOOL")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Update team status")
        print("2. Show progress summary")
        print("3. Exit")
        
        try:
            choice = int(input("\nSelect option: "))
            
            if choice == 1:
                update_team_status()
            elif choice == 2:
                show_progress_summary()
            elif choice == 3:
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 