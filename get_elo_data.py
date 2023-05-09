import pandas as pd
import random


ELO_DATA_PATH = "./mlb_elo_latest.csv"

elo = pd.read_csv(ELO_DATA_PATH)

TEAMS = pd.unique(list((elo.loc[:,"team1"])))


DIVISIONS = {"AL EAST": ["TBD", "BAL", "NYY", "BOS","TOR"],
             "AL CENTRAL": ["CLE", "MIN", "KCR", "DET", "CHW"],
             "AL WEST": ["ANA", "OAK", "SEA", "TEX", "HOU"],
             "NL EAST": ["PHI", "ATL", "FLA", "NYM", "WSN"],
             "NL Central": ["CHC", "CIN", "MIL", "PIT", "STL"],
             "NL WEST": ["ARI", "COL", "LAD", "SDP", "SFG"] }

# print(elo)


standings = pd.DataFrame(columns= ["Team", "Division", "Wins", "Loses", "Won_Div", "Won_Wildcard"])
standings["Team"] = TEAMS




def get_current_record(elo_data: pd.DataFrame, team_name: str) -> dict:
    wins: int = 0
    loses: int = 0 
    home_games = elo_data.loc[(elo_data['team1'] == team_name) , ["team1", "team2", "score1", "score2"]]
    away_games = elo_data.loc[(elo_data['team2'] == team_name) , ["team1", "team2", "score1", "score2"]]
    home_games = home_games.dropna()
    away_games = away_games.dropna()

    home_wins = (home_games['score1'] > home_games['score2']).sum()
    home_loses = (home_games['score1'] < home_games['score2']).sum()
    away_wins =  (away_games['score2'] > away_games['score1']).sum()
    away_loses =  (away_games['score2'] < away_games['score1']).sum()

    wins = home_wins + away_wins
    loses = home_loses + away_loses
    record = {"team": team_name, "wins": wins, "loses": loses}
    return(record)    

def simulate_game(prob: float)->int:
    """return 1 for home win 0 for away win"""
    if random.random() < prob:
        return(2)
    else:
        return(0)
    

def fill_in_regular_season(elo_original: pd.DataFrame) -> pd.DataFrame:
    # elo = drop_playoff_games(elo)
    # elo = elo.assign(score4 = lambda x: (simulate_game(x.rating_prob1) if pd.isnull(x.score1) else  5 ), axis =1)
    elo = elo_original.copy(deep=True)
    elo['score1'] = elo['score1'].fillna(elo.apply(lambda x: simulate_game(x['rating_prob1']) if pd.isnull(x['score1']) else x['score1'], axis=1))
    elo['score2'] = elo['score2'].fillna(1)

    return elo

def drop_playoff_games(elo: pd.DataFrame) -> pd.DataFrame:
    elo = elo[elo['team1'].notna()]
    return(elo)

def simulate_season(elo: pd.DataFrame, num_sims: int  =1000)->pd.DataFrame:
    seasons = []
    for i in range(0, num_sims):
        season = fill_in_regular_season(elo_original=elo)
        records =[]
        for j in TEAMS:
            record = get_current_record(elo_data=season, team_name= j)
            records.append(record)
        result = pd.DataFrame.from_dict(records)
        seasons.append(result)
    all_seasons = pd.concat([df[['team', 'wins', 'loses']] for df in seasons]).groupby('team').agg(list)
    return(all_seasons)



# Create a function that maps each team to its division
def get_division(team):
    for division, teams in DIVISIONS.items():
        if team in teams:
            return division
    return "Unknown"



# sim.to_csv("./2000_test.csv")


def process_projection(df:pd.DataFrame)-> pd.DataFrame:
    df['total_wins'] = df['wins'].apply(sum)

# Sort the dataframe by the total number of wins in descending order
    df = df.sort_values(by='total_wins', ascending=False)

# Create a new column that contains the division for each team
    df['division'] = df['team'].apply(get_division)

    sorted_df = df.sort_values(by=['division', 'total_wins'],  ascending=[True, False])
    return(sorted_df)


def won_divison(df: pd.DataFrame)-> bool:
    # Define a function to determine if a team had the most wins in a given year
    def team_had_most_wins(x):
        print("X IS ")
        wins = x['wins']
        print(wins)

        bool_lists = [val == max([wins[i] for wins in df['wins']]) for i, val in enumerate(wins)]
        print(bool_lists)
        print(type(bool_lists))

        # return [w == max(division_wins) for w in wins]
        return bool_lists

# Group the dataframe by division and apply the team_had_most_wins function to each group
    div_winners = df.groupby('division').apply(lambda x: team_had_most_wins(x)).to_list()
    print(div_winners.index)
    df['div_winner'] = div_winners

# Print the resulting dataframe
    return(df)




full_season = fill_in_regular_season(elo)
# print(full_season)

record = get_current_record(full_season, "PHI") 

sim = simulate_season(elo=elo, num_sims=3)
sim = sim.reset_index()

sim = process_projection(sim)
print(sim.groupby('division'))
# bool_lists = sim['wins'].apply(lambda row: [val == max(row) for val in row])
sim = won_divison(sim)
print(sim)
