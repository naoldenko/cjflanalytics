
# CJFL Manual Data Entry Instructions

## Overview
Since automated web scraping was not successful, you'll need to manually collect and enter real player data from the CJFL website and individual team websites.

## Data Sources

### Primary Sources:
1. **CJFL Official Website**: https://www.cjfl.org/
   - Look for "League Leaders" section
   - Check "All-Canadians" section
   - Find "Players of the Week" section
   - Look for team rosters or statistics

2. **Individual Team Websites**:
   - Each team has their own website with roster information
   - Team websites are listed in the template file

### Secondary Sources:
- Team social media accounts (Facebook, Twitter, Instagram)
- Local news articles about teams
- Team programs or media guides

## How to Enter Data

### Step 1: Collect Player Information
1. Visit https://www.cjfl.org/
2. Navigate to team pages or statistics sections
3. Collect player names, positions, and statistics
4. Note the season/year for the data

### Step 2: Use the Template
1. Open `data/cjfl_comprehensive_template.csv` in Excel or Google Sheets
2. Replace placeholder entries with real player data
3. Enter actual statistics for each player
4. Save the file

### Step 3: Import to Dashboard
1. Replace the current `data/cjfl_stats.csv` with your real data
2. Ensure the column headers match the existing format
3. Test the dashboard to ensure it works with real data

## Required Data Fields

For each player, you need:
- **Player Name**: Full name of the player
- **Team**: Team name (exactly as listed)
- **Position**: QB, RB, WR, TE, OL, DL, LB, DB, K, or P
- **Season**: Year (2024, 2023, 2022, etc.)
- **Games Played**: Number of games played
- **Passing Yards**: Total passing yards (for QBs)
- **Rushing Yards**: Total rushing yards (for RBs, QBs)
- **Receiving Yards**: Total receiving yards (for WRs, TEs, RBs)
- **Touchdowns**: Total touchdowns scored
- **Tackles**: Total tackles (for defensive players)
- **Sacks**: Total sacks (for defensive players)
- **Interceptions**: Total interceptions (for defensive players)

## Tips for Data Collection

1. **Start with League Leaders**: The CJFL website likely has statistical leaders
2. **Check Team Rosters**: Individual team websites often have current rosters
3. **Use Multiple Sources**: Combine data from official site and team sites
4. **Be Consistent**: Use the same format for all entries
5. **Validate Data**: Cross-reference statistics when possible

## Example Entry

```
Player Name: John Smith
Team: Calgary Colts
Position: QB
Season: 2024
Games Played: 10
Passing Yards: 2500
Rushing Yards: 300
Receiving Yards: 0
Touchdowns: 25
Tackles: 0
Sacks: 0
Interceptions: 0
```

## Next Steps

1. Visit the CJFL website and start collecting data
2. Use the template file to organize your findings
3. Enter real player statistics
4. Replace the generated data with authentic information
5. Test the analytics dashboard with real data

## Support

If you need help with data collection or entry, consider:
- Contacting individual teams directly
- Reaching out to the CJFL office
- Using social media to find team rosters
- Checking local sports news websites
