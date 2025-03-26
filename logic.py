import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load Data
def load_pickle(file_path):
    with open(file_path, "rb") as file:
        return pd.DataFrame(pickle.load(file))

df = load_pickle("match_information.pkl")
wicket = load_pickle("wicket.pkl")
total_runs_player = load_pickle("total_runs_player.pkl")
wicket_by_bowler = load_pickle("wicket_by_bowler.pkl")
bowler_wicket = load_pickle("bowler_wicket.pkl")
season_wise_runs = load_pickle("seaon_wise_runs_wise_players.pkl")
wicket_player_season = load_pickle("player_wicket.pkl")

class Logic:
    def __init__(self, df, wicket, total_runs_player, wicket_by_bowler, bowler_wicket, season_wise_runs, wicket_player_season):
        self.df = df
        self.wicket = wicket
        self.total_runs_player = total_runs_player
        self.wicket_by_bowler = wicket_by_bowler
        self.bowler_wicket = bowler_wicket
        self.season_wise_runs = season_wise_runs
        self.wicket_player_season = wicket_player_season

    def match_info(self):
        return self.df

    def season(self):
        season_choose = input('''\nChoose a season (2008-2023): ''')
        return season_choose

    def season_match_info(self, choose):
        if choose in self.df['season'].unique():
            return self.df[self.df['season'] == choose]
        else:
            return "No matches found for this season."

    def players_runs(self, player_name):
        player_runs = self.season_wise_runs[self.season_wise_runs['striker'] == player_name] \
            .groupby('season')['total_runs'].sum().reset_index()

        if not player_runs.empty:
            fig = px.line(player_runs, x="season", y="total_runs", title=f'{player_name} Runs Per Season', markers=True)
            fig.show()
        else:
            print("No data available for this player.")

        return player_runs

    def bowler_stats(self, bowler_name):
        bowler_wickets = self.wicket_player_season[self.wicket_player_season['bowler'] == bowler_name] \
            .groupby('season')['count'].sum().reset_index()

        if not bowler_wickets.empty:
            fig = px.bar(bowler_wickets, x="season", y="count", title=f'{bowler_name} Wickets Per Season')
            fig.show()
        else:
            print("No data available for this bowler.")

        return bowler_wickets

    def season_winner(self):
        season_winner_team = self.df.groupby('season').last()['match_winner'].reset_index()
        winner_count = season_winner_team['match_winner'].value_counts().reset_index()

        plt.figure(figsize=(10, 5))
        sns.barplot(x=winner_count['match_winner'], y=winner_count['count'])
        plt.xticks(rotation=90)
        plt.title("Season-Wise Winners Count")
        plt.xlabel("Team")
        plt.ylabel("Number of Wins")
        plt.show()

        return season_winner_team, winner_count

    def team_performance(self, team_name):
        team_matches = self.df[(self.df['team1'] == team_name) | (self.df['team2'] == team_name)]
        total_matches = len(team_matches)
        wins = team_matches[team_matches['match_winner'] == team_name]
        total_wins = len(wins)
        win_percentage = (total_wins / total_matches) * 100 if total_matches > 0 else 0

        print(f"🏏 {team_name} - Matches Played: {total_matches}, Wins: {total_wins}, Win %: {win_percentage:.2f}%")

        if not wins.empty:
            fig = px.line(wins, x="season", y="match_winner", title=f'{team_name} Wins Per Season', markers=True)
            fig.show()
        else:
            print(f"No win data available for {team_name}.")

        return team_matches


# Initialize Logic
if __name__ == "__main__":
    ob = Logic(df, wicket, total_runs_player, wicket_by_bowler, bowler_wicket, season_wise_runs, wicket_player_season)

    # Season Match Information
    selected_season = ob.season()
    match_information = ob.season_match_info(selected_season)
    print("Match Information:\n", match_information, "\n")

    # Player Performance
    player_name = input("Enter the player name: ")
    total_runs_player = ob.players_runs(player_name)
    print("Player Runs Data:\n", total_runs_player, "\n")

    # Bowler Performance
    bowler_name = input("Enter the bowler name: ")
    bowler_stats = ob.bowler_stats(bowler_name)
    print("Bowler Wickets Data:\n", bowler_stats, "\n")

    # Season Winner Data
    season_winner = ob.season_winner()
    print("Season Winners:\n", season_winner, "\n")

    # Team Performance
    team_name = input("Enter the team name: ")
    team_performance = ob.team_performance(team_name)
    print("Team Performance Data:\n", team_performance, "\n")
