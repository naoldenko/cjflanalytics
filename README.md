# 🏈 CJFL Analytics Dashboard

A comprehensive data collection and analytics system for the Canadian Junior Football League (CJFL), featuring real data collection tools, progress tracking, and interactive dashboards for player statistics analysis.

## 📊 Current Status

### ✅ **Real Data Collection System**
- **Active Data Collection**: System for collecting real CJFL statistics from team websites
- **Progress Tracking**: Real-time dashboard showing collection progress across all 20 CJFL teams
- **Manual Data Entry**: Interactive tools for entering and managing player statistics
- **Data Quality**: Real player data from multiple teams (Edmonton Wildcats, Calgary Colts, Saskatoon Hilltops, etc.)

### 📈 **Available Dashboards**
- **Main Analytics Dashboard** (`streamlit_app.py`): Full-featured analytics with real data
- **Progress Dashboard** (`progress_dashboard.py`): Data collection progress tracking
- **Legacy Dashboard** (`app.py`): Original multi-season dashboard

## 🚀 Quick Start

### Option 1: Main Analytics Dashboard (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the main analytics dashboard
streamlit run streamlit_app.py
```

### Option 2: Progress Dashboard
```bash
# View data collection progress
streamlit run progress_dashboard.py
```

### Option 3: Legacy Multi-Season Dashboard
```bash
# Run the original dashboard
streamlit run app.py
```

## 📊 Features

### Main Analytics Dashboard (`streamlit_app.py`)
- **Real Data Integration**: Works with actual CJFL player statistics
- **Interactive Filters**: Season, Team, Position, and Player search
- **Comprehensive Statistics**: 13 different stat categories including per-game metrics
- **Top 10 Players**: Bar charts for each stat category
- **Performance Trends**: Line charts showing player performance over time
- **Team Comparison**: Side-by-side team statistics comparison
- **Player Profiles**: Individual player radar charts with detailed stats
- **Data Export**: Download filtered data as CSV
- **Dark Mode Theme**: Modern dark interface with responsive design

### Progress Dashboard (`progress_dashboard.py`)
- **Collection Progress**: Real-time tracking of data collection from all 20 CJFL teams
- **Team Status**: Visual indicators for completed, in-progress, and not-started teams
- **Data Quality Metrics**: Analysis of collected data completeness and accuracy
- **Collection Tips**: Guidance for data collection from team websites
- **Progress Charts**: Visual representation of collection progress

### Data Collection Tools
- **Manual Data Entry** (`manual_data_entry.py`): Interactive tool for adding player data
- **Team Collection Scripts**: Automated tools for specific teams (e.g., `collect_calgary_colts_data.py`)
- **Progress Updates** (`update_progress.py`): CLI tool for updating collection status
- **Collection Planning** (`data_collection_plan.py`): Comprehensive plan for all 20 teams

## 🛠️ Data Collection System

### Available Teams for Data Collection
**✅ Ready for Collection (10 teams):**
- Calgary Colts, Edmonton Wildcats, Saskatoon Hilltops
- Edmonton Huskies, Kamloops Broncos, Langley Rams
- Prince George Kodiaks, Vancouver Island Raiders
- Hamilton Hurricanes, Ottawa Sooners

**❌ Not Available (10 teams):**
- Regina Thunder, Winnipeg Rifles, Okanagan Sun, Valley Huskers
- Westshore Rebels, London Beefeaters, Quinte Skyhawks
- St. Clair Saints, GTA Grizzlies, Sault Ste. Marie Cougars

### Data Collection Process
1. **Team Website Analysis**: Check team websites for player statistics
2. **Manual Data Entry**: Use the interactive entry tool to add player data
3. **Progress Tracking**: Monitor collection progress through the dashboard
4. **Quality Control**: Verify data accuracy and completeness
5. **Export and Analysis**: Use collected data in the main analytics dashboard

## 📁 Project Structure

```
cjflanalytics/
├── streamlit_app.py          # Main analytics dashboard (2024 season focus)
├── app.py                    # Legacy multi-season dashboard
├── progress_dashboard.py     # Data collection progress tracking
├── manual_data_entry.py     # Interactive data entry tool
├── data_collection_plan.py  # Comprehensive collection strategy
├── collect_calgary_colts_data.py  # Team-specific collector
├── update_progress.py       # Progress update CLI tool
├── utils.py                 # Helper functions for data processing
├── requirements.txt         # Python dependencies
├── run_dashboard.sh        # Easy launch script
├── README.md               # Project documentation
├── CJFL_DATA_COLLECTION_STARTED.md  # Data collection guide
├── MANUAL_DATA_ENTRY_INSTRUCTIONS.md # Entry tool guide
└── data/                   # Data directory
    ├── cjfl_stats.csv      # Main player statistics (real + sample data)
    ├── cjfl_real_data_template.csv  # Data template
    └── collection_progress.json     # Progress tracking
```

## 📈 Data Structure

The system uses real CJFL player statistics with the following structure:

| Column | Description | Data Type |
|--------|-------------|-----------|
| Player Name | Player's full name | String |
| Team | CJFL team name | String |
| Position | Player position (QB, RB, WR, DB, LB, K) | String |
| Season | Year (2024) | Integer |
| Games Played | Number of games played | Integer |
| Passing Yards | Total passing yards | Integer |
| Rushing Yards | Total rushing yards | Integer |
| Receiving Yards | Total receiving yards | Integer |
| Touchdowns | Total touchdowns scored | Integer |
| Tackles | Total tackles made | Integer |
| Sacks | Total sacks recorded | Integer |
| Interceptions | Total interceptions | Integer |

## 🎨 UI Features

### Dark Mode Theme
- Modern dark color scheme with high contrast
- Consistent styling across all components
- Responsive design for different screen sizes

### Interactive Elements
- Hover tooltips on all charts
- Real-time filtering and updates
- Tabbed interface for different stat categories
- Sidebar filters for easy data exploration

### Data Visualization
- Interactive bar charts using Plotly Express
- Multi-line trend charts for player performance
- Radar charts for player profiles
- Team comparison grouped bar charts
- Progress tracking pie charts

## 🔧 Customization

### Adding New Teams
1. Update `data_collection_plan.py` with team information
2. Add team website analysis in collection scripts
3. Use manual data entry tool to add player data
4. Update progress tracking

### Modifying Visualizations
- Edit chart configurations in `utils.py`
- Customize colors and themes in dashboard files
- Add new chart types as needed

### Extending Data Collection
- Create new team-specific collection scripts
- Add new data sources and APIs
- Implement automated data scraping

## 📊 Current Data Status

### Real Data Collected
- **Edmonton Wildcats**: 50+ players with complete statistics
- **Calgary Colts**: 10+ players with real data
- **Saskatoon Hilltops**: Sample data for testing
- **Additional Teams**: Sample data for demonstration

### Data Quality
- **Real Statistics**: Actual player performance data
- **Multiple Positions**: QB, RB, DB, LB, K positions covered
- **Complete Records**: Games played, yards, touchdowns, tackles, sacks
- **Season Focus**: 2024 season data (primary focus)

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
**Best for**: Quick deployment with automatic updates

1. **Push your code to GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repository**
4. **Set the app path to `streamlit_app.py`**
5. **Deploy!**

### Render
**Best for**: Professional deployment with custom domains

1. **Create account on [render.com](https://render.com)**
2. **Connect your GitHub repository**
3. **Choose "Web Service"**
4. **Configure build settings**
5. **Deploy!**

## 🎯 Use Cases

### For Data Collectors
- Track collection progress across all teams
- Enter and manage player statistics
- Monitor data quality and completeness
- Export collected data for analysis

### For Coaches and Scouts
- Identify top performers by position
- Track player development over time
- Compare team strengths and weaknesses
- Discover emerging talent

### For Analysts
- Analyze performance trends
- Generate statistical reports
- Export filtered data for further analysis
- Create player comparison reports

### For Fans and Media
- Interactive player exploration
- Team performance insights
- Historical data visualization
- Player profile deep dives

## 🔮 Future Enhancements

### Planned Features
- [ ] Player comparison tool (side-by-side up to 3 players)
- [ ] Advanced statistical analysis
- [ ] Season-over-season team performance tracking
- [ ] Player injury tracking and analysis
- [ ] Real-time data integration
- [ ] Mobile-optimized interface
- [ ] Automated data scraping from team websites
- [ ] API integration for live statistics

### Potential Integrations
- Live game statistics
- Social media sentiment analysis
- Player social media integration
- Advanced analytics and predictions
- Official CJFL data feeds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes. For commercial use with real CJFL data, ensure compliance with league data usage policies.

## 📞 Support

For questions or issues:
- Check the documentation above
- Review the code comments
- Test with the provided data
- Ensure all dependencies are installed

---

**Note**: This system now includes real CJFL data collection capabilities. The main dashboard works with actual player statistics, while the progress dashboard tracks data collection from all 20 CJFL teams. For production use with real CJFL statistics, ensure proper data sourcing and compliance with league policies.
