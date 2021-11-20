import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import json
from dash import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("rain.csv")
df.reset_index(inplace=True)
years = df["Year"].unique()

app.layout = html.Div(children=[
    html.H1(children='Rainfall-Deforestation'),
    dcc.Dropdown(id='slct_year',
                 options=[
                     {"label": year, "value":year} for year in years
                 ],
                 multi=False,
                 value=2005,
                 style={"widht": "40%"}
                 ),
    html.Div(id='output_container', children=[]),

    dcc.Graph(
        id='example-graph',
        figure={}
    )
])

india_states = json.load(open("states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

#state_id_map
df["id"] = df["State"].apply(lambda x: state_id_map[x])
df['Year']=df['Year'].astype(int)


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='example-graph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig = px.choropleth(
                dff,
        locations='id',
        geojson=india_states,
        color='Annual Rainfall',
        scope='asia',
        hover_name="State",
        hover_data=['State'],
        color_continuous_scale='matter'
    )
    return container, fig

if __name__ == '__main__':
    app.run_server(debug=False)
# fig = px.choropleth(
#         df,
#         locations='id',
#         geojson=india_states,
#         color='rainfall(in mm)',
#         scope='asia',
#         hover_name="place",
#         hover_data=['rainfall(in mm)'],
#         color_continuous_scale='matter'
    
#     )