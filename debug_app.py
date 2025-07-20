#!/usr/bin/env python3

import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(page_title="CJFL Debug", layout="wide")

st.title("🔍 CJFL Data Debug")

# Load data
data = load_data()

st.header("📊 Data Information")
st.write(f"**Data shape:** {data.shape}")
st.write(f"**Total players:** {len(data)}")
st.write(f"**Total teams:** {len(data['Team'].unique())}")
st.write(f"**Teams:** {sorted(data['Team'].unique())}")

st.header("📋 Team Breakdown")
team_counts = data['Team'].value_counts()
st.write(team_counts)

st.header("📊 Sample Data")
st.dataframe(data.head(10))

st.header("🔍 Data Source Check")
if len(data['Team'].unique()) >= 8:
    st.success("✅ Full dataset loaded (8+ teams)")
elif len(data['Team'].unique()) >= 4:
    st.warning("⚠️ Partial dataset loaded (4+ teams)")
else:
    st.error("❌ Limited dataset loaded (< 4 teams)")

# Test the same logic as the main app
total_players = len(data['Player Name'].unique())
total_teams = len(data['Team'].unique())

if total_teams >= 8:
    st.success(f"✅ Real CJFL Data: {total_players} players from {total_teams} teams")
elif total_teams >= 4:
    st.warning(f"⚠️ Partial Real Data: {total_players} players from {total_teams} teams")
else:
    st.info(f"📊 Sample Data: {total_players} players from {total_teams} teams") 