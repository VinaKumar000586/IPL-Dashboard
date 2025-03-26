import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

# Set page configuration with background image
st.set_page_config(page_title="🏏 IPL Analytics Dashboard", layout="wide")

# Custom CSS for Background & Styling
st.markdown(
    """
    <style>
        /* Background Image */
        .main {
            background: url('https://raw.githubusercontent.com/VinaKumar000586/Hospitality-domain-hotel-revenue/main/ipl_bg.jpg') no-repeat center center fixed;
            background-size: cover;
        }
        
        /* Custom Fonts */
        h1, h2, h3 {
            color: #ffffff !important;
            text-align: center;
        }

        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #1e3d59;
        }

        /* Text Color */
        .stTextInput label, .stSelectbox label, .stRadio label {
            color: white !important;
        }

        /* DataFrame Style */
        .stDataFrame {
            border-radius: 10px;
        }

    </style>
    """,
    
    unsafe_allow_html=True
    
)

# Function to load pickle files
def load_pickle(file_path):
    with open(file_path, "rb") as file:
        return pd.DataFrame(pickle.load(file))

# Load Data
df = load_pickle("match_information.pkl")
season_wise_runs = load_pickle("seaon_wise_runs_wise_players.pkl")
wicket_player_season = load_pickle("player_wicket.pkl")

# Sidebar with IPL Logo
st.sidebar.image("https://www.iplt20.com/assets/images/ipl-logo-new-old.png", use_container_width=True)
st.sidebar.title("🏏 IPL Analytics Dashboard")
page = st.sidebar.radio(
    "Select Analysis",
    ["🏆 Season Analysis", "📊 Player Performance", "🎯 Bowler Stats", "🏏 Team Performance", "📅 Match Information"]
)

# Season Analysis
if page == "🏆 Season Analysis":
    st.image("winner.jpg", width=300,use_container_width=True)
    st.title("🏆 IPL Season-Wise Analysis")

    season_winner_team = df.groupby('season').last()['match_winner'].reset_index()
    winner_count = season_winner_team['match_winner'].value_counts().reset_index()
    winner_count.columns = ["Team", "Seasons Won"]

    st.subheader("🏆 Season Winners")
    st.dataframe(season_winner_team)

    st.subheader("🏅 Season-Wise Winner Count")
    fig = px.bar(winner_count, x="Team", y="Seasons Won", title="🏆 Number of Titles Won by Teams", text_auto=True)
    st.plotly_chart(fig)

# Player Performance
elif page == "📊 Player Performance":
    st.image("D:\IPL 2008 to 2023\IPL-2020-player-performance-report-card-e1605804856917.jpg", width=500,use_container_width=True)
    st.title("📊 Player Performance")

    player_list = season_wise_runs['striker'].unique().tolist()
    player_name = st.selectbox("Select Player:", player_list, index=0)

    if player_name:
        player_runs = season_wise_runs[season_wise_runs['striker'] == player_name].groupby('season')['total_runs'].sum().reset_index()

        st.subheader(f"🏏 {player_name} - Runs Per Season")
        st.dataframe(player_runs)

        if not player_runs.empty:
            fig = px.line(player_runs, x="season", y="total_runs", title=f'{player_name} Runs Per Season', markers=True)
            st.plotly_chart(fig)
        else:
            st.warning("⚠ No data available for this player.")

# Bowler Stats
elif page == "🎯 Bowler Stats":
    st.image("D:\IPL 2008 to 2023\IPL-2025-Complete-Bowlers-List-for-All-10-Teams.jpg", width=400,use_container_width=True)
    st.title("🎯 Bowler Statistics")

    bowler_list = wicket_player_season['bowler'].unique().tolist()
    bowler_name = st.selectbox("Select Bowler:", bowler_list, index=0)

    if bowler_name:
        bowler_wickets = wicket_player_season[wicket_player_season['bowler'] == bowler_name].groupby('season')['count'].sum().reset_index()

        st.subheader(f"🎯 {bowler_name} - Wickets Per Season")
        st.dataframe(bowler_wickets)

        if not bowler_wickets.empty:
            fig = px.bar(bowler_wickets, x="season", y="count", title=f'{bowler_name} Wickets Per Season', text_auto=True)
            st.plotly_chart(fig)
        else:
            st.warning("⚠ No data available for this bowler.")

# Team Performance
elif page == "🏏 Team Performance":
    st.image("D:\IPL 2008 to 2023\Ipl-timelime-2024.jpg", width=300,use_container_width=True)
    st.title("🏏 Team Performance")

    team_list = pd.concat([df['team_1'], df['team_2']]).unique().tolist()
    team_name = st.selectbox("Select Team:", team_list, index=0)

    if team_name:
        team_matches = df[(df['team_1'] == team_name) | (df['team_2'] == team_name)]
        season_performance = team_matches.groupby('season').agg(
            total_matches=('match_id', 'count'),
            wins=('match_winner', lambda x: (x == team_name).sum()),
        ).reset_index()
        season_performance['losses'] = season_performance['total_matches'] - season_performance['wins']

        venue_count = team_matches['venue'].value_counts().reset_index()
        venue_count.columns = ['Venue', 'Matches Played']

        st.subheader(f"📊 {team_name} - Performance Overview")
        st.dataframe(season_performance)

        fig = px.bar(season_performance, x="season", y=["wins", "losses"], barmode="group",
                     title=f"{team_name} Wins & Losses Per Season", text_auto=True)
        st.plotly_chart(fig)

        st.subheader("📍 Matches Played at Different Venues")
        st.dataframe(venue_count)

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
