import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import os

# Set page configuration
st.set_page_config(page_title="🏏 IPL Analytics Dashboard", layout="wide")

# Custom CSS Styling
st.markdown(
    """
    <style>
        .main { background: url('https://raw.githubusercontent.com/VinaKumar000586/Hospitality-domain-hotel-revenue/main/ipl_bg.jpg') no-repeat center center fixed; background-size: cover; }
        h1, h2, h3 { color: #ffffff !important; text-align: center; }
        [data-testid="stSidebar"] { background-color: #1e3d59; }
        .stTextInput label, .stSelectbox label, .stRadio label { color: white !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to load pickle files with error handling
def load_pickle(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return pd.DataFrame(pickle.load(file))
    else:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

# Load Data
df = load_pickle("match_information.pkl")
season_wise_runs = load_pickle("seaon_wise_runs_wise_players.pkl")
wicket_player_season = load_pickle("player_wicket.pkl")

# Check if required columns exist in datasets
required_columns = {'match_id', 'team_1', 'team_2', 'match_winner', 'season', 'venue'}
if not required_columns.issubset(df.columns):
    st.error(f"Missing columns in dataset: {required_columns - set(df.columns)}")

# Sidebar with IPL Logo
st.sidebar.image("https://www.iplt20.com/assets/images/ipl-logo-new-old.png", use_container_width=True)
st.sidebar.title("🏏 IPL Analytics Dashboard")
page = st.sidebar.radio("Select Analysis", ["🏆 Season Analysis", "📊 Player Performance", "🎯 Bowler Stats", "🏏 Team Performance", "📅 Match Information"])

# Season Analysis
if page == "🏆 Season Analysis":
    st.image("IPL-winners-list-from-2008-to-2024-blog (1).png", use_container_width=True)
    st.title("🏆 IPL Season-Wise Analysis")
    
    if 'season' in df.columns and 'match_winner' in df.columns:
        season_winner_team = df.groupby('season').last()['match_winner'].reset_index()
        winner_count = season_winner_team['match_winner'].value_counts().reset_index()
        winner_count.columns = ["Team", "Seasons Won"]
        
        st.subheader("🏆 Season Winners")
        st.dataframe(season_winner_team)
        
        st.subheader("🏅 Season-Wise Winner Count")
        fig = px.bar(winner_count, x="Team", y="Seasons Won", title="🏆 Number of Titles Won by Teams", text_auto=True)
        st.plotly_chart(fig)
    else:
        st.error("Required columns missing for season analysis")

# Player Performance
elif page == "📊 Player Performance":
    st.image("IPL-2020-player-performance-report-card-e1605804856917.jpg", use_container_width=True)
    st.title("📊 Player Performance")
    
    if 'striker' in season_wise_runs.columns:
        player_list = season_wise_runs['striker'].dropna().unique().tolist()
        player_name = st.selectbox("Select Player:", player_list)
        
        if player_name:
            player_runs = season_wise_runs[season_wise_runs['striker'] == player_name].groupby('season')['total_runs'].sum().reset_index()
            
            st.subheader(f"🏏 {player_name} - Runs Per Season")
            st.dataframe(player_runs)
            
            fig = px.line(player_runs, x="season", y="total_runs", title=f'{player_name} Runs Per Season', markers=True)
            st.plotly_chart(fig)
    else:
        st.error("Required columns missing for player analysis")

# Bowler Stats
elif page == "🎯 Bowler Stats":
    st.image("IPL-2025-Complete-Bowlers-List-for-All-10-Teams.jpg", use_container_width=True)
    st.title("🎯 Bowler Statistics")
    
    if 'bowler' in wicket_player_season.columns:
        bowler_list = wicket_player_season['bowler'].dropna().unique().tolist()
        bowler_name = st.selectbox("Select Bowler:", bowler_list)
        
        if bowler_name:
            bowler_wickets = wicket_player_season[wicket_player_season['bowler'] == bowler_name].groupby('season')['count'].sum().reset_index()
            
            st.subheader(f"🎯 {bowler_name} - Wickets Per Season")
            st.dataframe(bowler_wickets)
            
            fig = px.bar(bowler_wickets, x="season", y="count", title=f'{bowler_name} Wickets Per Season', text_auto=True)
            st.plotly_chart(fig)
    else:
        st.error("Required columns missing for bowler analysis")

# Team Performance
elif page == "🏏 Team Performance":
    st.image("Ipl-timelime-2024.jpg", use_container_width=True)
    st.title("🏏 Team Performance")
    
    if 'team_1' in df.columns and 'team_2' in df.columns:
        team_list = pd.concat([df['team_1'], df['team_2']]).dropna().unique().tolist()
        team_name = st.selectbox("Select Team:", team_list)
        
        if team_name:
            team_matches = df[(df['team_1'] == team_name) | (df['team_2'] == team_name)]
            season_performance = team_matches.groupby('season').agg(
                total_matches=('match_id', 'count'),
                wins=('match_winner', lambda x: (x == team_name).sum()),
            ).reset_index()
            season_performance['losses'] = season_performance['total_matches'] - season_performance['wins']
            
            st.subheader(f"📊 {team_name} - Performance Overview")
            st.dataframe(season_performance)
            
            fig = px.bar(season_performance, x="season", y=["wins", "losses"], barmode="group", title=f"{team_name} Wins & Losses Per Season", text_auto=True)
            st.plotly_chart(fig)
    else:
        st.error("Required columns missing for team performance analysis")

# Match Information
elif page == "📅 Match Information":
    st.image("https://www.iplt20.com/assets/images/ipl-logo-new-old.png", use_container_width=300)
    st.title("📅 Match Information")
    
    season_list = df['season'].unique().tolist()
    selected_season = st.selectbox("Select Season:", season_list, index=0)
    
    if selected_season:
        season_matches = df[df['season'] == selected_season]
        match_info_cols = ["match_date", "team_1", "team_2", "venue", "match_winner", "player_of_match", "city"]
        available_cols = [col for col in match_info_cols if col in df.columns]
        
        st.subheader(f"📅 Matches in Season {selected_season}")
        st.dataframe(season_matches[available_cols])
        
        fig = px.histogram(season_matches, x="venue", title=f"Matches Played in Different Venues - {selected_season}", text_auto=True)
        st.plotly_chart(fig)
