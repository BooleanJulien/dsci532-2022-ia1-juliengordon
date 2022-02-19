import pandas as pd
import altair as alt
from dash import Dash, html, dcc, Input, Output
alt.data_transformers.disable_max_rows()

gap_data = pd.read_csv('world-data-gapminder_raw.csv')

gap_data = gap_data.groupby(['sub_region', 'year']).mean()

app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    dcc.Dropdown(
        id='ycol-widget', value='life_expectancy',
        options=[{'label': i, 'value': i} for i in gap_data.columns]),
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'})])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair(ycol):
    chart = alt.Chart(gap_data.reset_index()).mark_line().encode(
    x='year',
    y=ycol,
    color='sub_region',
    tooltip='sub_region').interactive()
    return chart.to_html()

def update_output(ycol):
    return plot_altair(ycol)

if __name__ == '__main__':
    app.run_server(debug=True)


