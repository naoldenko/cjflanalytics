#!/usr/bin/env python3

import pandas as pd
from utils import load_data

print("=== TESTING DATA LOADING ===")

# Test the load_data function
data = load_data()
print(f"Data shape: {data.shape}")
print(f"Teams: {sorted(data['Team'].unique())}")
print(f"Total teams: {len(data['Team'].unique())}")
print(f"Total players: {len(data)}")
print("\nTeam counts:")
print(data['Team'].value_counts())

# Test direct CSV loading
print("\n=== DIRECT CSV LOADING ===")
try:
    direct_data = pd.read_csv('data/cjfl_stats.csv')
    print(f"Direct CSV shape: {direct_data.shape}")
    print(f"Direct CSV teams: {sorted(direct_data['Team'].unique())}")
    print(f"Direct CSV total teams: {len(direct_data['Team'].unique())}")
except Exception as e:
    print(f"Error loading CSV: {e}")

# Check if template file exists
print("\n=== TEMPLATE FILE CHECK ===")
try:
    template_data = pd.read_csv('data/cjfl_real_data_template.csv')
    print(f"Template shape: {template_data.shape}")
    print(f"Template teams: {sorted(template_data['Team'].unique())}")
    print(f"Template total teams: {len(template_data['Team'].unique())}")
except Exception as e:
    print(f"Error loading template: {e}") 