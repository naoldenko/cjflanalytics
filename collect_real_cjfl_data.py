#!/usr/bin/env python3
"""
CJFL Real Data Collection Script
Helps collect actual CJFL statistics from official sources
"""

import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import re

def get_cjfl_official_stats():
    """
    Attempt to scrape CJFL official website for statistics
    """
    print("🔍 Attempting to collect data from CJFL official website...")
    
    # CJFL official website URLs to check
    cjfl_urls = [
        "https://www.cjfl.org/",
        "https://www.cjfl.org/statistics",
        "https://www.cjfl.org/league-leaders",
        "https://www.cjfl.org/players-of-the-week"
    ]
    
    collected_data = []
    
    for url in cjfl_urls:
        try:
            print(f"Checking: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for statistics tables
            tables = soup.find_all('table')
            for table in tables:
                print(f"Found table with {len(table.find_all('tr'))} rows")
                
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            continue
    
    return collected_data

def get_team_websites():
    """
    List of CJFL team websites for manual data collection
    """
    team_websites = {
        # Prairie Football Conference (PFC)
        "Calgary Colts": "https://calgarycolts.com/",
        "Edmonton Wildcats": "https://edmontonwildcats.com/",
        "Edmonton Huskies": "https://edmontonhuskies.com/",
        "Regina Thunder": "https://reginathunder.com/",
        "Saskatoon Hilltops": "https://saskatoonhilltops.com/",
        "Winnipeg Rifles": "https://winnipegrifles.com/",
        
        # British Columbia Football Conference (BCFC)
        "Vancouver Island Raiders": "https://viraiders.com/",
        "Okanagan Sun": "https://okanagansun.com/",
        "Langley Rams": "https://langleyrams.com/",
        "Westshore Rebels": "https://westshorerebels.com/",
        "Valley Huskers": "https://valleyhuskers.com/",
        "Kamloops Broncos": "https://kamloopsbroncos.com/",
        "Prince George Kodiaks": "https://pgkodiaks.com/",
        
        # Ontario Football Conference (OFC)
        "London Beefeaters": "https://londonbeefeaters.com/",
        "Hamilton Hurricanes": "https://hamiltonhurricanes.com/",
        "Ottawa Sooners": "https://ottawasooners.com/",
        "Quinte Skyhawks": "https://quinteskyhawks.com/",
        "St. Clair Saints": "https://stclairsaints.com/",
        "GTA Grizzlies": "https://gtagrizzlies.com/",
        "Sault Ste. Marie Cougars": "https://saultcougars.com/"
    }
    
    return team_websites

def create_data_template():
    """
    Create a template CSV file for manual data entry
    """
    template_data = {
        'Player Name': [],
        'Team': [],
        'Position': [],
        'Season': [],
        'Games Played': [],
        'Passing Yards': [],
        'Rushing Yards': [],
        'Receiving Yards': [],
        'Touchdowns': [],
        'Tackles': [],
        'Sacks': [],
        'Interceptions': []
    }
    
    # Create template with example entries
    example_players = [
        # Example QB
        ['John Smith', 'Calgary Colts', 'QB', 2024, 10, 2500, 300, 0, 25, 0, 0, 0],
        # Example RB
        ['Mike Johnson', 'Edmonton Wildcats', 'RB', 2024, 12, 0, 1200, 400, 15, 0, 0, 0],
        # Example WR
        ['David Wilson', 'Saskatoon Hilltops', 'WR', 2024, 11, 0, 50, 800, 8, 0, 0, 0],
        # Example DB
        ['Chris Davis', 'Regina Thunder', 'DB', 2024, 10, 0, 0, 0, 0, 45, 0, 3],
        # Example LB
        ['Tom Brown', 'Winnipeg Rifles', 'LB', 2024, 12, 0, 0, 0, 0, 65, 5, 2]
    ]
    
    for player in example_players:
        for i, key in enumerate(template_data.keys()):
            template_data[key].append(player[i])
    
    df = pd.DataFrame(template_data)
    df.to_csv('data/cjfl_real_data_template.csv', index=False)
    print("✅ Created template file: data/cjfl_real_data_template.csv")
    return df

def display_data_collection_instructions():
    """
    Display instructions for collecting real CJFL data
    """
    print("\n" + "="*80)
    print("🏈 CJFL REAL DATA COLLECTION INSTRUCTIONS")
    print("="*80)
    
    print("\n📋 STEP 1: Access Official Sources")
    print("- CJFL Official Website: https://www.cjfl.org/")
    print("- Look for 'Statistics', 'League Leaders', or 'Players of the Week' sections")
    print("- Check individual team websites (listed below)")
    
    print("\n📋 STEP 2: Team Websites to Check")
    team_sites = get_team_websites()
    for team, url in team_sites.items():
        print(f"- {team}: {url}")
    
    print("\n📋 STEP 3: Data to Collect")
    print("For each player, collect:")
    print("- Full Name")
    print("- Team")
    print("- Position (QB, RB, WR, TE, OL, DL, LB, DB, K, P)")
    print("- Season (2024)")
    print("- Games Played")
    print("- Passing Yards (QBs only)")
    print("- Rushing Yards (RBs, QBs)")
    print("- Receiving Yards (WRs, TEs, RBs)")
    print("- Touchdowns")
    print("- Tackles (defensive players)")
    print("- Sacks (DL, LB)")
    print("- Interceptions (DB, LB)")
    
    print("\n📋 STEP 4: Use the Template")
    print("- Open 'data/cjfl_real_data_template.csv'")
    print("- Replace example entries with real data")
    print("- Save as 'data/cjfl_stats.csv'")
    
    print("\n📋 STEP 5: Alternative Sources")
    print("- Team social media accounts")
    print("- Local news articles")
    print("- Team programs or media guides")
    print("- Contact teams directly for statistics")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("- Ensure all statistics are from the 2024 season")
    print("- Use consistent team names as listed above")
    print("- Verify data accuracy when possible")
    print("- Include all players, not just starters")

def check_available_data_sources():
    """
    Check what data sources are currently available
    """
    print("\n🔍 CHECKING AVAILABLE DATA SOURCES")
    print("="*50)
    
    # Check CJFL official site
    try:
        response = requests.get("https://www.cjfl.org/", timeout=5)
        if response.status_code == 200:
            print("✅ CJFL official website is accessible")
        else:
            print("❌ CJFL official website returned status:", response.status_code)
    except Exception as e:
        print(f"❌ Cannot access CJFL official website: {e}")
    
    # Check a few team websites
    team_sites = get_team_websites()
    test_teams = ["Calgary Colts", "Edmonton Wildcats", "Saskatoon Hilltops"]
    
    for team in test_teams:
        if team in team_sites:
            try:
                response = requests.get(team_sites[team], timeout=5)
                if response.status_code == 200:
                    print(f"✅ {team} website is accessible")
                else:
                    print(f"❌ {team} website returned status: {response.status_code}")
            except Exception as e:
                print(f"❌ Cannot access {team} website: {e}")

def main():
    """
    Main function to help collect real CJFL data
    """
    print("🏈 CJFL REAL DATA COLLECTION TOOL")
    print("="*50)
    
    # Check available data sources
    check_available_data_sources()
    
    # Create data template
    print("\n📝 Creating data template...")
    create_data_template()
    
    # Display instructions
    display_data_collection_instructions()
    
    # Attempt to get some data from CJFL site
    print("\n🔍 Attempting to collect data from CJFL official site...")
    cjfl_data = get_cjfl_official_stats()
    
    if cjfl_data:
        print(f"✅ Found {len(cjfl_data)} records from CJFL official site")
    else:
        print("❌ No data found from CJFL official site")
        print("💡 You'll need to manually collect data from team websites")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Visit the team websites listed above")
    print("2. Collect player statistics for the 2024 season")
    print("3. Use the template file to organize the data")
    print("4. Replace the current cjfl_stats.csv with real data")
    print("5. Test the dashboard with real statistics")

if __name__ == "__main__":
    main() 