import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import json
from dash import Input, Output
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("rain.csv")
df_avg = pd.read_csv("Data.csv")
df.reset_index(inplace=True)
df_avg.reset_index(inplace=True)
years = df["Year"].unique()

india_states = json.load(open("states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
df["id"] = df["State"].apply(lambda x: state_id_map[x])
df_avg["id"] = df_avg['place'].apply(lambda x: state_id_map[x])
df['Year'] = df['Year'].astype(int)

# scatterplotRain = px.scatter(
#         data_frame=df_avg,
#         x="place",
#         y="rainfall(in mm)",
#         color="place",
#         hover_data=['place'],
#         height=550
#     )
# scatterplotRain.update_traces(textposition='top center')

# scatterplotDef = px.scatter(
#         data_frame=df_avg,
#         x="place",
#         y="deforestation(in Ha)",
#         color="place",
#         hover_data=['place'],
#         height=550
#     )
# scatterplotDef.update_traces(textposition='top center')

# Choropleth map of Avg Rainfall and Deforestation (2001-2015)
figAvgDef = px.choropleth(
    df_avg,
    locations="id",
    geojson=india_states,
    color="deforestation(in Ha)",
    hover_name="place",
    scope="asia",
    color_continuous_scale='deep')

figAvgDef.update_geos(fitbounds="locations")
figAvgDef.update_layout(title_text='Average Deforestation by States')

figAvgRain = px.choropleth(
    df_avg,
    locations="id",
    geojson=india_states,
    color="rainfall(in mm)",
    hover_name='place',
    scope='asia',
    color_continuous_scale='matter')

figAvgRain.update_geos(fitbounds="locations")
figAvgRain.update_layout(title_text='Average Rainfall by States')


# Scatter plots of Rainfall and Deforestation Year wise
scatterplotRain = px.scatter(
    data_frame=df,
    x="State",
    y="Annual Rainfall",
    color="State",
    size='Year',
    hover_data=['State'],
    height=600
)
scatterplotRain.update_traces(textposition='top center')
scatterplotRain.update_layout(title_text='Annual Rainfall By States')

scatterplotDef = px.scatter(
    data_frame=df,
    x="State",
    y="DEF",
    color="State",
    size='Year',
    hover_data=['State'],
    height=600
)
scatterplotDef.update_traces(textposition='top center')
scatterplotDef.update_layout(title_text='Annual Deforestation By States')

# Rainfall and Deforestation by States using Bar chart
fig = go.Figure(data=[
    go.Bar(name='Average Rainfall',
           x=df_avg['place'], y=df_avg['rainfall(in mm)']),
    go.Bar(name='Average Deforestation',
           x=df_avg['place'], y=df_avg['deforestation(in Ha)'])
])
fig.update_layout(barmode='group')
fig.update_layout(title_text='Rainfall and Deforestation by States')

app.layout = html.Div(children=[
    html.H1(children='Rainfall-Deforestation'),
    dcc.Dropdown(id='slct_year',
                 options=[
                     {"label": year, "value": year} for year in years
                 ],
                 multi=False,
                 value=2005,
                 style={"width": "40%"}
                 ),
    html.Div(id='output_container', children=[]),

    html.Div(
        [
            html.Div([
                dcc.Graph(
                    id='rainfall-graph',
                    figure={})
            ], className='six columns'
            ),

            html.Div([
                dcc.Graph(
                    id='deforestation-graph',
                    figure={})
            ], className="six columns"
            )
        ], className="row"
    ),
    html.Div(
        [
            html.Div([
                dcc.Graph(
                    id='scatterrain',
                    figure=scatterplotRain)
            ], className='six columns'
            ),

            html.Div([
                dcc.Graph(
                    id='scatterdef',
                    figure=scatterplotDef)
            ], className="six columns"
            )
        ], className="row"
    ),
    html.Div(
        [
            html.Div([
                dcc.Graph(
                    id='chororain',
                    figure=figAvgRain)
            ], className='six columns'
            ),

            html.Div([
                dcc.Graph(
                    id='chorodef',
                    figure=figAvgDef)
            ], className="six columns"
            )
        ], className="row"
    ),
    html.Div([
        dcc.Graph(id='rain_def', figure=fig)
    ], className="row")

])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='rainfall-graph', component_property='figure'),
     Output(component_id='deforestation-graph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Year: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]

    # annual Rainfall
    figRain = px.choropleth(
        dff,
        locations='id',
        geojson=india_states,
        color='Annual Rainfall',
        scope='asia',
        hover_name="State",
        hover_data=['State'],
        color_continuous_scale='deep'
    )
    figRain.update_geos(fitbounds="locations", visible=False)
    figRain.update_layout(title_text='Annual Rainfall by States')

    # annual deforestation
    figDef = px.choropleth(
        dff,
        locations='id',
        geojson=india_states,
        color='DEF',
        scope='asia',
        hover_name="State",
        hover_data=['State'],
        color_continuous_scale='matter'
    )
    figDef.update_geos(fitbounds="locations", visible=False)
    figDef.update_layout(title_text='Annual Deforestation by States')
    return container, figRain, figDef


if __name__ == '__main__':
    app.run_server(debug=False)
