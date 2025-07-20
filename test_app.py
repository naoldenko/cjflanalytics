#!/usr/bin/env python3
"""
Test script for CJFL Analytics Dashboard
This script tests all major components to ensure they work correctly.
"""

import pandas as pd
import numpy as np
from utils import load_data, filter_data, create_player_profile, create_team_comparison

def test_data_loading():
    """Test data loading functionality"""
    print("Testing data loading...")
    try:
        data = load_data()
        print(f"✅ Data loaded successfully! Shape: {data.shape}")
        print(f"✅ Columns: {list(data.columns)}")
        print(f"✅ Seasons: {sorted(data['Season'].unique())}")
        print(f"✅ Teams: {len(data['Team'].unique())} teams")
        print(f"✅ Positions: {sorted(data['Position'].unique())}")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_filtering():
    """Test data filtering functionality"""
    print("\nTesting data filtering...")
    try:
        data = load_data()
        
        # Test season filtering
        filtered = filter_data(data, [2023], [], [], "")
        print(f"✅ Season filtering: {len(filtered)} records for 2023")
        
        # Test team filtering
        teams = data['Team'].unique()[:2]
        filtered = filter_data(data, [], list(teams), [], "")
        print(f"✅ Team filtering: {len(filtered)} records for {len(teams)} teams")
        
        # Test position filtering
        positions = ['QB', 'RB']
        filtered = filter_data(data, [], [], positions, "")
        print(f"✅ Position filtering: {len(filtered)} records for {len(positions)} positions")
        
        # Test player search
        player_name = data['Player Name'].iloc[0]
        filtered = filter_data(data, [], [], [], player_name.split()[0])
        print(f"✅ Player search: {len(filtered)} records found")
        
        return True
    except Exception as e:
        print(f"❌ Data filtering failed: {e}")
        return False

def test_visualizations():
    """Test visualization functions"""
    print("\nTesting visualizations...")
    try:
        data = load_data()
        
        # Test player profile creation
        player_data = data[data['Player Name'] == data['Player Name'].iloc[0]]
        profile_fig = create_player_profile(player_data)
        print(f"✅ Player profile chart created: {type(profile_fig)}")
        
        # Test team comparison
        teams = data['Team'].unique()[:2]
        comparison_fig = create_team_comparison(data, teams[0], teams[1])
        print(f"✅ Team comparison chart created: {type(comparison_fig)}")
        
        return True
    except Exception as e:
        print(f"❌ Visualization testing failed: {e}")
        return False

def test_data_quality():
    """Test data quality and statistics"""
    print("\nTesting data quality...")
    try:
        data = load_data()
        
        # Check for missing values
        missing_values = data.isnull().sum()
        print(f"✅ Missing values: {missing_values.sum()} total")
        
        # Check data ranges
        print(f"✅ Season range: {data['Season'].min()} - {data['Season'].max()}")
        print(f"✅ Games played range: {data['Games Played'].min()} - {data['Games Played'].max()}")
        print(f"✅ Passing yards range: {data['Passing Yards'].min()} - {data['Passing Yards'].max()}")
        print(f"✅ Rushing yards range: {data['Rushing Yards'].min()} - {data['Rushing Yards'].max()}")
        print(f"✅ Receiving yards range: {data['Receiving Yards'].min()} - {data['Receiving Yards'].max()}")
        
        # Check for realistic values
        assert data['Games Played'].min() >= 0, "Games played should be non-negative"
        assert data['Passing Yards'].min() >= 0, "Passing yards should be non-negative"
        assert data['Rushing Yards'].min() >= 0, "Rushing yards should be non-negative"
        assert data['Receiving Yards'].min() >= 0, "Receiving yards should be non-negative"
        assert data['Touchdowns'].min() >= 0, "Touchdowns should be non-negative"
        assert data['Tackles'].min() >= 0, "Tackles should be non-negative"
        assert data['Sacks'].min() >= 0, "Sacks should be non-negative"
        assert data['Interceptions'].min() >= 0, "Interceptions should be non-negative"
        
        print("✅ All data quality checks passed!")
        return True
    except Exception as e:
        print(f"❌ Data quality check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🏈 CJFL Analytics Dashboard - Component Tests")
    print("=" * 50)
    
    tests = [
        test_data_loading,
        test_filtering,
        test_visualizations,
        test_data_quality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The dashboard is ready to run.")
        print("\nTo start the dashboard, run:")
        print("streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 