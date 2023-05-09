import pandas as pd



elo_url ="https://projects.fivethirtyeight.com/mlb-api/mlb_elo_latest.csv"

df = pd.read_csv(elo_url)
print(df)

