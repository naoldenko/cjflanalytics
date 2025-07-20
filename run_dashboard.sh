#!/bin/bash

# CJFL Analytics Dashboard Launcher
echo "🏈 CJFL Analytics Dashboard"
echo "=========================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit, pandas, plotly, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Check if data exists, if not it will be generated
echo "📊 Checking data..."
if [ ! -f "data/cjfl_stats.csv" ]; then
    echo "📊 Generating sample data..."
    python3 -c "from utils import load_data; load_data()"
fi

# Launch the dashboard
echo "🚀 Starting CJFL Analytics Dashboard..."
echo "🌐 Open your browser and go to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the dashboard"
echo ""

streamlit run streamlit_app.py 