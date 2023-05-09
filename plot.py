import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import ast
import numpy as np
from get_elo_data import process_projection

# Create the subplots
COLORS_DF = pd.read_csv("./mlb_color.csv")



df = pd.read_csv("./2000_test.csv")

df['wins'] = df['wins'].apply(ast.literal_eval)


df = process_projection(df)
# x = list(df.loc[df['team'] == "PHI"]['wins'])
# x =np.sort(x[0])
# print(x)
# fig = go.Figure(data=[go.Histogram(x=x, nbinsx=30)])
# fig.show()

print(df['wins'])
print(df.columns)
team_titles_order = list(df['team'])
team_titles_order = np.array(team_titles_order).reshape(6, 5).T.ravel().tolist()
print(team_titles_order)
fig = make_subplots(rows=5, cols=6, subplot_titles=team_titles_order)
# Loop over each team in the DataFrame
for i, team in enumerate(df['team']):
    col = (i // 5) + 1
    row = (i % 5) + 1
    color = COLORS_DF.loc[COLORS_DF['abbreviation'] == team.lower()]['primary_color'].values[0]
    # Add the histogram trace to the subplot


    x = list(df.loc[df['team'] == team]['wins'])
    x =np.sort(x[0])


    trace = go.Histogram(x=x, name=team, histnorm='percent', marker=dict(color=color))
    fig.append_trace(trace, row=row, col=col)
        
    fig.update_xaxes(title_text='Wins', range=[40,120], row=row, col=col)
    # #fig.add_annotation(x=0.5, y=1.15, xref='paper', yref='paper', 
    #                    text=f"{team}", showarrow=False, font=dict(size=12), 
    #                    row=row, col=col)
    

# Update the subplot layout
fig.update_layout(
    height=1000,
    width=1200,
    title='Distribution of Wins by Team',
)
#fig.update_xaxes(title_text='Wins')

# Show the plot
pyo.iplot(fig)