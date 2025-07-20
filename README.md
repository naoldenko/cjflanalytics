# 🏈 CJFL Analytics Dashboard

A comprehensive Streamlit web dashboard for tracking and visualizing Canadian Junior Football League (CJFL) player statistics for the past 3 seasons (2022–2024).

## 📊 Features

### Dashboard Components
- **Interactive Filters**: Season, Team, Position, and Player search
- **Top 10 Players**: Bar charts for each stat category (Passing Yards, Rushing Yards, Receiving Yards, Touchdowns, Tackles, Sacks)
- **Performance Trends**: Line charts showing player performance over seasons
- **Team Comparison**: Side-by-side team statistics comparison
- **Player Profiles**: Individual player radar charts with detailed stats
- **Emerging Talent**: Highlighting players under 21 with strong performance
- **Data Export**: Download filtered data as CSV

### Visualizations
- Interactive bar charts using Plotly Express
- Multi-line trend charts for player performance
- Radar charts for player profiles
- Team comparison grouped bar charts
- Dark mode theme with modern styling

## 🚀 Quick Start

### Local Development

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd cjflanalytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to view the dashboard

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

## 📁 Project Structure

```
cjflanalytics/
├── streamlit_app.py      # Main Streamlit dashboard application
├── utils.py              # Helper functions for data processing and visualization
├── requirements.txt      # Python dependencies
├── .streamlit/config.toml # Streamlit configuration
├── render.yaml           # Render deployment configuration
├── packages.txt          # System dependencies
├── README.md            # Project documentation
├── test_app.py          # Component testing script
├── demo_data.py         # Data showcase script
├── run_dashboard.sh     # Easy launch script for Streamlit version
└── data/                # Data directory (auto-created)
    └── cjfl_stats.csv  # Generated player statistics (auto-created)
```

## 📈 Data Structure

The dashboard uses simulated CJFL player statistics with the following columns:

| Column | Description | Data Type |
|--------|-------------|-----------|
| Player Name | Player's full name | String |
| Team | CJFL team name | String |
| Position | Player position (QB, RB, WR, etc.) | String |
| Season | Year (2022, 2023, 2024) | Integer |
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
- Modern dark color scheme
- High contrast for readability
- Consistent styling across all components

### Interactive Elements
- Hover tooltips on all charts
- Responsive layout for different screen sizes
- Real-time filtering and updates

### Navigation
- Sidebar filters for easy data exploration
- Tabbed interface for different stat categories
- Clear section headers and organization

## 🔧 Customization

### Adding Real Data
To integrate real CJFL data:

1. Replace the `generate_cjfl_data()` function in `utils.py` with your data loading logic
2. Update the data structure to match your CSV format
3. Modify the `load_data()` function to point to your data source

### Modifying Visualizations
- Edit chart configurations in `utils.py`
- Customize colors and themes in `streamlit_app.py`
- Add new chart types as needed

### Adding New Features
- Extend the sidebar filters in `streamlit_app.py`
- Create new helper functions in `utils.py`
- Add new visualization sections

## 📊 Data Sources

**Current Implementation**: Simulated data for demonstration purposes

**Real Data Integration**: 
- CJFL official statistics website
- League databases
- Team-provided statistics
- API endpoints (if available)

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations

### Performance
- Cached data loading for faster performance
- Efficient filtering and processing
- Responsive design for various devices

## 🎯 Use Cases

### For Coaches and Scouts
- Identify top performers by position
- Track player development over seasons
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

### Potential Integrations
- Live game statistics
- Social media sentiment analysis
- Player social media integration
- Advanced analytics and predictions

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
- Test with the provided simulated data
- Ensure all dependencies are installed

---

**Note**: This dashboard uses simulated data for demonstration. For production use with real CJFL statistics, ensure proper data sourcing and compliance with league policies.
