#!/usr/bin/env python3
"""
Calgary Colts Data Collection Script
Helps collect real CJFL statistics from Calgary Colts sources
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import time

class CalgaryColtsCollector:
    def __init__(self):
        self.team_name = "Calgary Colts"
        self.website = "https://calgarycolts.com/"
        self.social_media = {
            "facebook": "https://www.facebook.com/calgarycolts",
            "twitter": "https://twitter.com/calgarycolts"
        }
        self.contact_email = "info@calgarycolts.com"
        self.data_file = "data/cjfl_stats.csv"
        self.template_file = "data/cjfl_real_data_template.csv"
        
    def check_website_sections(self):
        """Check what sections are available on the Calgary Colts website"""
        print("🔍 CHECKING CALGARY COLTS WEBSITE SECTIONS")
        print("=" * 50)
        
        try:
            response = requests.get(self.website, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for navigation menu
                nav_links = soup.find_all('a', href=True)
                print("📋 Found website sections:")
                
                sections = []
                for link in nav_links:
                    href = link.get('href', '').lower()
                    text = link.get_text(strip=True)
                    
                    if any(keyword in href or keyword in text.lower() for keyword in 
                          ['roster', 'players', 'team', 'stats', 'statistics', 'schedule', 'news']):
                        sections.append(f"- {text}: {href}")
                
                if sections:
                    for section in sections:
                        print(section)
                else:
                    print("- No specific roster/players sections found")
                    print("- Will need to explore the website manually")
                
                return True
            else:
                print(f"❌ Website returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error accessing website: {str(e)}")
            return False
    
    def search_for_player_data(self):
        """Search for player data on the website"""
        print("\n🔍 SEARCHING FOR PLAYER DATA")
        print("=" * 40)
        
        try:
            response = requests.get(self.website, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for player-related content
                player_keywords = ['player', 'roster', 'team', 'stats', 'statistics']
                found_content = []
                
                for keyword in player_keywords:
                    elements = soup.find_all(text=lambda text: text and keyword.lower() in text.lower())
                    for element in elements[:5]:  # Limit to first 5 matches
                        found_content.append(f"- Found '{keyword}' in: {element.strip()[:100]}...")
                
                if found_content:
                    print("📋 Found potential player-related content:")
                    for content in found_content:
                        print(content)
                else:
                    print("❌ No obvious player data found on main page")
                    print("💡 Need to explore deeper or contact team directly")
                
                return True
            else:
                print(f"❌ Website returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error searching website: {str(e)}")
            return False
    
    def create_data_collection_plan(self):
        """Create a detailed plan for collecting Calgary Colts data"""
        print("\n📋 CALGARY COLTS DATA COLLECTION PLAN")
        print("=" * 50)
        
        plan = f"""
🏈 CALGARY COLTS DATA COLLECTION STRATEGY

📋 TEAM INFORMATION:
- Team: Calgary Colts
- Conference: PFC (Prairie Football Conference)
- Website: {self.website}
- Contact: {self.contact_email}

🔍 DATA SOURCES TO CHECK (in order):

1. WEBSITE EXPLORATION:
   - Visit: {self.website}
   - Look for: Roster, Players, Team, Statistics sections
   - Check: News/Updates for game reports
   - Search for: 2024 season information

2. SOCIAL MEDIA:
   - Facebook: {self.social_media['facebook']}
   - Twitter: {self.social_media['twitter']}
   - Look for: Game updates, player highlights, roster announcements

3. DIRECT CONTACT:
   - Email: {self.contact_email}
   - Request: 2024 season player statistics
   - Ask for: Official roster and player stats

4. ALTERNATIVE SOURCES:
   - Local news articles
   - CJFL official website
   - Team press releases
   - Game reports from opponents

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
- Focus on 2024 season only
- Include all players, not just starters
- If exact stats aren't available, note what is available
- Document the source of each piece of data
- Update progress as you collect

📝 TEMPLATE USAGE:
- Use: {self.template_file}
- Save collected data to: {self.data_file}
- Format: CSV with headers from template

🎯 NEXT STEPS:
1. Manually visit the website and explore
2. Check social media for recent updates
3. Contact the team via email
4. Document any data found
5. Update progress tracking
"""
        
        print(plan)
        return plan
    
    def update_progress(self, status="in_progress", players_collected=0, notes=""):
        """Update the progress tracking for Calgary Colts"""
        progress_file = "data/collection_progress.json"
        
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                progress = json.load(f)
        else:
            progress = {
                "start_date": datetime.now().isoformat(),
                "teams": {},
                "total_players_collected": 0,
                "total_teams_completed": 0,
                "last_updated": datetime.now().isoformat()
            }
        
        if self.team_name not in progress["teams"]:
            progress["teams"][self.team_name] = {
                "status": "not_started",
                "players_collected": 0,
                "data_sources_checked": [],
                "notes": "",
                "last_updated": datetime.now().isoformat()
            }
        
        progress["teams"][self.team_name]["status"] = status
        progress["teams"][self.team_name]["players_collected"] += players_collected
        progress["teams"][self.team_name]["notes"] = notes
        progress["teams"][self.team_name]["last_updated"] = datetime.now().isoformat()
        progress["total_players_collected"] += players_collected
        progress["last_updated"] = datetime.now().isoformat()
        
        os.makedirs("data", exist_ok=True)
        with open(progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
        
        print(f"✅ Progress updated: {self.team_name} - {status}")
    
    def add_player_data(self, player_data):
        """Add collected player data to the CSV file"""
        try:
            # Load existing data
            if os.path.exists(self.data_file):
                df = pd.read_csv(self.data_file)
            else:
                # Use template structure
                df = pd.read_csv(self.template_file)
                df = df[df['Team'] != self.team_name]  # Remove template entries for this team
            
            # Add new player data
            new_row = pd.DataFrame([player_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save updated data
            df.to_csv(self.data_file, index=False)
            print(f"✅ Added player data: {player_data['Player Name']}")
            
        except Exception as e:
            print(f"❌ Error adding player data: {str(e)}")
    
    def manual_data_entry_guide(self):
        """Provide guide for manual data entry"""
        print("\n📝 MANUAL DATA ENTRY GUIDE")
        print("=" * 40)
        
        guide = f"""
📋 MANUAL DATA ENTRY PROCESS:

1. VISIT WEBSITE:
   - Go to: {self.website}
   - Explore all sections thoroughly
   - Look for roster, players, or team information

2. CHECK SOCIAL MEDIA:
   - Facebook: {self.social_media['facebook']}
   - Twitter: {self.social_media['twitter']}
   - Look for recent posts about players or games

3. CONTACT TEAM:
   - Email: {self.contact_email}
   - Request: 2024 season player statistics
   - Be specific about what data you need

4. RECORD DATA:
   - Use the template: {self.template_file}
   - Add each player found
   - Include all available statistics
   - Note the source of each piece of data

5. UPDATE PROGRESS:
   - Run this script to update progress
   - Document what was found/not found
   - Move to next team when complete

📊 DATA FIELDS TO FILL:
- Player Name: Full name
- Team: Calgary Colts
- Position: QB, RB, WR, TE, OL, DL, LB, DB, K, P
- Season: 2024
- Games Played: Number of games in 2024
- Passing Yards: For QBs only
- Rushing Yards: For RBs, QBs
- Receiving Yards: For WRs, TEs, RBs
- Touchdowns: Total TDs
- Tackles: For defensive players
- Sacks: For DL, LB
- Interceptions: For DB, LB

💡 TIPS:
- If exact stats aren't available, use 0 or leave blank
- Document what you find vs. what you don't find
- Take screenshots of useful pages
- Note any contact responses
"""
        
        print(guide)
        return guide

def main():
    """Main function to run Calgary Colts data collection"""
    collector = CalgaryColtsCollector()
    
    print("🏈 CALGARY COLTS DATA COLLECTION")
    print("=" * 50)
    
    # Check website sections
    collector.check_website_sections()
    
    # Search for player data
    collector.search_for_player_data()
    
    # Create collection plan
    collector.create_data_collection_plan()
    
    # Provide manual entry guide
    collector.manual_data_entry_guide()
    
    # Update progress to in_progress
    collector.update_progress(status="in_progress", notes="Started data collection process")
    
    print(f"\n🎯 READY TO START COLLECTING DATA FROM CALGARY COLTS!")
    print("=" * 60)
    print("📋 Next steps:")
    print("1. Visit the website and explore")
    print("2. Check social media accounts")
    print("3. Contact the team via email")
    print("4. Document any data found")
    print("5. Update progress when done")
    print(f"\n📁 Progress tracking: data/collection_progress.json")
    print(f"📊 Data file: {collector.data_file}")

if __name__ == "__main__":
    main() 