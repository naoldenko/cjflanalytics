#!/usr/bin/env python3
"""
CJFL Data Collection Plan and Progress Tracker
Detailed plan for collecting real CJFL statistics from specific teams
"""

import pandas as pd
import json
import os
import requests
from datetime import datetime

class CJFLDataCollector:
    def __init__(self):
        self.teams = {
            # Prairie Football Conference (PFC)
            "Calgary Colts": {
                "website": "https://calgarycolts.com/",
                "social_media": ["https://www.facebook.com/calgarycolts", "https://twitter.com/calgarycolts"],
                "contact": "info@calgarycolts.com",
                "priority": 1,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Active website, good social media presence",
                "conference": "PFC"
            },
            "Edmonton Huskies": {
                "website": "https://edmontonhuskies.com/",
                "social_media": ["https://www.facebook.com/edmontonhuskies", "https://twitter.com/edmontonhuskies"],
                "contact": "info@edmontonhuskies.com",
                "priority": 2,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Rival to Wildcats",
                "conference": "PFC"
            },
            "Edmonton Wildcats": {
                "website": "https://edmontonwildcats.com/",
                "social_media": ["https://www.facebook.com/edmontonwildcats", "https://twitter.com/edmontonwildcats"],
                "contact": "info@edmontonwildcats.com",
                "priority": 1,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Active website, strong local presence",
                "conference": "PFC"
            },
            "Regina Thunder": {
                "website": "https://reginathunder.com/",
                "social_media": ["https://www.facebook.com/reginathunder", "https://twitter.com/reginathunder"],
                "contact": "info@reginathunder.com",
                "priority": 2,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Strong program, good website",
                "conference": "PFC"
            },
            "Saskatoon Hilltops": {
                "website": "https://saskatoonhilltops.com/",
                "social_media": ["https://www.facebook.com/saskatoonhilltops", "https://twitter.com/saskatoonhilltops"],
                "contact": "info@saskatoonhilltops.com",
                "priority": 1,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Multiple championships, good record keeping",
                "conference": "PFC"
            },
            "Winnipeg Rifles": {
                "website": "https://winnipegrifles.com/",
                "social_media": ["https://www.facebook.com/winnipegrifles", "https://twitter.com/winnipegrifles"],
                "contact": "info@winnipegrifles.com",
                "priority": 2,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Established program",
                "conference": "PFC"
            },
            
            # British Columbia Football Conference (BCFC)
            "Kamloops Broncos": {
                "website": "https://kamloopsbroncos.com/",
                "social_media": ["https://www.facebook.com/kamloopsbroncos", "https://twitter.com/kamloopsbroncos"],
                "contact": "info@kamloopsbroncos.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "BCFC team",
                "conference": "BCFC"
            },
            "Langley Rams": {
                "website": "https://langleyrams.com/",
                "social_media": ["https://www.facebook.com/langleyrams", "https://twitter.com/langleyrams"],
                "contact": "info@langleyrams.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "BCFC team",
                "conference": "BCFC"
            },
            "Okanagan Sun": {
                "website": "https://okanagansun.com/",
                "social_media": ["https://www.facebook.com/okanagansun", "https://twitter.com/okanagansun"],
                "contact": "info@okanagansun.com",
                "priority": 2,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "Strong BC program",
                "conference": "BCFC"
            },
            "Prince George Kodiaks": {
                "website": "https://pgkodiaks.com/",
                "social_media": ["https://www.facebook.com/pgkodiaks", "https://twitter.com/pgkodiaks"],
                "contact": "info@pgkodiaks.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "BCFC team",
                "conference": "BCFC"
            },
            "Valley Huskers": {
                "website": "https://valleyhuskers.com/",
                "social_media": ["https://www.facebook.com/valleyhuskers", "https://twitter.com/valleyhuskers"],
                "contact": "info@valleyhuskers.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "BCFC team",
                "conference": "BCFC"
            },
            "Vancouver Island Raiders": {
                "website": "https://viraiders.com/",
                "social_media": ["https://www.facebook.com/viraiders", "https://twitter.com/viraiders"],
                "contact": "info@viraiders.com",
                "priority": 2,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "BCFC powerhouse",
                "conference": "BCFC"
            },
            "Westshore Rebels": {
                "website": "https://westshorerebels.com/",
                "social_media": ["https://www.facebook.com/westshorerebels", "https://twitter.com/westshorerebels"],
                "contact": "info@westshorerebels.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "BCFC team",
                "conference": "BCFC"
            },
            
            # Ontario Football Conference (OFC)
            "Hamilton Hurricanes": {
                "website": "https://hamiltonhurricanes.com/",
                "social_media": ["https://www.facebook.com/hamiltonhurricanes", "https://twitter.com/hamiltonhurricanes"],
                "contact": "info@hamiltonhurricanes.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            },
            "London Beefeaters": {
                "website": "https://londonbeefeaters.com/",
                "social_media": ["https://www.facebook.com/londonbeefeaters", "https://twitter.com/londonbeefeaters"],
                "contact": "info@londonbeefeaters.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            },
            "Ottawa Sooners": {
                "website": "https://ottawasooners.com/",
                "social_media": ["https://www.facebook.com/ottawasooners", "https://twitter.com/ottawasooners"],
                "contact": "info@ottawasooners.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            },
            "Quinte Skyhawks": {
                "website": "https://quinteskyhawks.com/",
                "social_media": ["https://www.facebook.com/quinteskyhawks", "https://twitter.com/quinteskyhawks"],
                "contact": "info@quinteskyhawks.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            },
            "St. Clair Saints": {
                "website": "https://stclairsaints.com/",
                "social_media": ["https://www.facebook.com/stclairsaints", "https://twitter.com/stclairsaints"],
                "contact": "info@stclairsaints.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            },
            "GTA Grizzlies": {
                "website": "https://gtagrizzlies.com/",
                "social_media": ["https://www.facebook.com/gtagrizzlies", "https://twitter.com/gtagrizzlies"],
                "contact": "info@gtagrizzlies.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            },
            "Sault Ste. Marie Cougars": {
                "website": "https://saultcougars.com/",
                "social_media": ["https://www.facebook.com/saultcougars", "https://twitter.com/saultcougars"],
                "contact": "info@saultcougars.com",
                "priority": 3,
                "status": "not_started",
                "data_sources": ["website", "social_media", "direct_contact"],
                "notes": "OFC team",
                "conference": "OFC"
            }
        }
        
        self.progress_file = "data/collection_progress.json"
        self.load_progress()
    
    def load_progress(self):
        """Load existing progress data"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        else:
            self.progress = {
                "start_date": datetime.now().isoformat(),
                "teams": {},
                "total_players_collected": 0,
                "total_teams_completed": 0,
                "last_updated": datetime.now().isoformat()
            }
    
    def save_progress(self):
        """Save progress data"""
        self.progress["last_updated"] = datetime.now().isoformat()
        os.makedirs("data", exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def check_team_availability(self, team_name):
        """Check if a team's website is accessible"""
        if team_name not in self.teams:
            return False, "Team not found"
        
        team_info = self.teams[team_name]
        website = team_info["website"]
        
        try:
            response = requests.get(website, timeout=10)
            if response.status_code == 200:
                return True, "Website accessible"
            else:
                return False, f"Website returned status {response.status_code}"
        except Exception as e:
            return False, f"Website not accessible: {str(e)}"
    
    def check_all_teams_availability(self):
        """Check availability of all teams"""
        print("🔍 CHECKING ALL CJFL TEAMS AVAILABILITY")
        print("=" * 60)
        
        results = {}
        
        for conference in ["PFC", "BCFC", "OFC"]:
            print(f"\n📋 {conference} TEAMS:")
            print("-" * 40)
            
            conference_teams = {name: info for name, info in self.teams.items() if info["conference"] == conference}
            
            for team_name, team_info in conference_teams.items():
                is_available, message = self.check_team_availability(team_name)
                status = "✅ Available" if is_available else "❌ Not Available"
                
                print(f"{team_name:<25} {status}")
                print(f"{'':25} {message}")
                print(f"{'':25} Website: {team_info['website']}")
                print()
                
                results[team_name] = {
                    "available": is_available,
                    "message": message,
                    "website": team_info["website"],
                    "conference": conference
                }
        
        return results
    
    def update_team_status(self, team_name, status, notes=""):
        """Update the status of a team's data collection"""
        if team_name not in self.progress["teams"]:
            self.progress["teams"][team_name] = {
                "status": "not_started",
                "players_collected": 0,
                "data_sources_checked": [],
                "notes": "",
                "last_updated": datetime.now().isoformat()
            }
        
        self.progress["teams"][team_name]["status"] = status
        self.progress["teams"][team_name]["notes"] = notes
        self.progress["teams"][team_name]["last_updated"] = datetime.now().isoformat()
        self.save_progress()
    
    def add_players_to_team(self, team_name, player_count):
        """Add collected players to team progress"""
        if team_name not in self.progress["teams"]:
            self.progress["teams"][team_name] = {
                "status": "in_progress",
                "players_collected": 0,
                "data_sources_checked": [],
                "notes": "",
                "last_updated": datetime.now().isoformat()
            }
        
        self.progress["teams"][team_name]["players_collected"] += player_count
        self.progress["total_players_collected"] += player_count
        self.save_progress()
    
    def get_priority_teams(self):
        """Get teams sorted by priority"""
        return sorted(self.teams.items(), key=lambda x: x[1]["priority"])
    
    def get_next_team_to_collect(self):
        """Get the next team that needs data collection"""
        for team_name, team_info in self.get_priority_teams():
            if team_name not in self.progress["teams"] or self.progress["teams"][team_name]["status"] == "not_started":
                return team_name, team_info
        return None, None
    
    def display_collection_plan(self):
        """Display the detailed collection plan"""
        print("🏈 CJFL DATA COLLECTION PLAN")
        print("=" * 60)
        
        for conference in ["PFC", "BCFC", "OFC"]:
            print(f"\n📋 {conference} TEAMS:")
            print("-" * 40)
            
            conference_teams = {name: info for name, info in self.teams.items() if info["conference"] == conference}
            
            for team_name, team_info in conference_teams.items():
                status = self.progress["teams"].get(team_name, {}).get("status", "not_started")
                players = self.progress["teams"].get(team_name, {}).get("players_collected", 0)
                priority = team_info["priority"]
                
                print(f"✅ {team_name}")
                print(f"   Website: {team_info['website']}")
                print(f"   Priority: {priority}")
                print(f"   Status: {status}")
                print(f"   Players Collected: {players}")
                print(f"   Notes: {team_info['notes']}")
                print()
    
    def display_progress_summary(self):
        """Display overall progress summary"""
        print("\n📊 COLLECTION PROGRESS SUMMARY")
        print("=" * 40)
        
        total_teams = len(self.teams)
        completed_teams = sum(1 for team in self.progress["teams"].values() if team["status"] == "completed")
        in_progress_teams = sum(1 for team in self.progress["teams"].values() if team["status"] == "in_progress")
        not_started_teams = total_teams - completed_teams - in_progress_teams
        
        print(f"Total Teams: {total_teams}")
        print(f"Completed: {completed_teams}")
        print(f"In Progress: {in_progress_teams}")
        print(f"Not Started: {not_started_teams}")
        print(f"Total Players Collected: {self.progress['total_players_collected']}")
        
        if self.progress["start_date"]:
            start_date = datetime.fromisoformat(self.progress["start_date"])
            days_elapsed = (datetime.now() - start_date).days
            print(f"Days Elapsed: {days_elapsed}")
    
    def get_team_collection_guide(self, team_name):
        """Get detailed collection guide for a specific team"""
        if team_name not in self.teams:
            return None
        
        team_info = self.teams[team_name]
        
        guide = f"""
🏈 DATA COLLECTION GUIDE: {team_name}
{'=' * 50}

📋 TEAM INFORMATION:
- Website: {team_info['website']}
- Contact: {team_info['contact']}
- Conference: {team_info['conference']}
- Priority: {team_info['priority']}
- Notes: {team_info['notes']}

🔍 DATA SOURCES TO CHECK:
"""
        
        for source in team_info['data_sources']:
            if source == "website":
                guide += f"- Website: {team_info['website']}\n"
                guide += "  * Look for 'Roster', 'Players', 'Statistics' sections\n"
                guide += "  * Check for game reports or player profiles\n"
            elif source == "social_media":
                guide += "- Social Media:\n"
                for social in team_info['social_media']:
                    guide += f"  * {social}\n"
                guide += "  * Look for game updates and player highlights\n"
            elif source == "direct_contact":
                guide += f"- Direct Contact: {team_info['contact']}\n"
                guide += "  * Email for official statistics\n"
                guide += "  * Request 2024 season player data\n"
        
        guide += """
📊 DATA TO COLLECT:
- Player Name (Full Name)
- Position (QB, RB, WR, TE, OL, DL, LB, DB, K, P)
- Games Played (2024 season)
- Passing Yards (QBs only)
- Rushing Yards (RBs, QBs)
- Receiving Yards (WRs, TEs, RBs)
- Touchdowns
- Tackles (defensive players)
- Sacks (DL, LB)
- Interceptions (DB, LB)

💡 COLLECTION TIPS:
- Start with the team's roster page
- Look for game reports or statistics sections
- Check social media for player highlights
- Contact the team directly if needed
- Focus on 2024 season data only
- Include all players, not just starters

📝 TEMPLATE USAGE:
- Use 'data/cjfl_real_data_template.csv'
- Add collected data to the template
- Save as 'data/cjfl_stats.csv' when ready
"""
        
        return guide

def main():
    """Main function to run the data collection plan"""
    collector = CJFLDataCollector()
    
    print("🏈 CJFL DATA COLLECTION PLAN AND PROGRESS TRACKER")
    print("=" * 60)
    
    # Check all teams availability
    collector.check_all_teams_availability()
    
    # Display collection plan
    collector.display_collection_plan()
    
    # Display progress summary
    collector.display_progress_summary()
    
    # Get next team to collect
    next_team, team_info = collector.get_next_team_to_collect()
    
    if next_team:
        print(f"\n🎯 NEXT TEAM TO COLLECT: {next_team}")
        print("=" * 50)
        
        guide = collector.get_team_collection_guide(next_team)
        print(guide)
        
        print("\n📋 QUICK ACTIONS:")
        print(f"1. Visit: {team_info['website']}")
        print(f"2. Contact: {team_info['contact']}")
        print("3. Use the template to record data")
        print("4. Update progress when done")
    else:
        print("\n🎉 All teams have been processed!")
    
    print(f"\n📁 Progress saved to: {collector.progress_file}")

if __name__ == "__main__":
    main() 