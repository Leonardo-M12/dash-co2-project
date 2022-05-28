from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


### Setup ###

app = Dash(__name__)


co2_data = pd.read_csv("owid-co2-data.csv")

pan_co2 = co2_data.loc[co2_data["iso_code"] == "PAN"]
cri_co2 = co2_data.loc[co2_data["iso_code"] == "CRI"]
nic_co2 = co2_data.loc[co2_data["iso_code"] == "NIC"]
hnd_co2 = co2_data.loc[co2_data["iso_code"] == "HND"]
slv_co2 = co2_data.loc[co2_data["iso_code"] == "SLV"]
gtm_co2 = co2_data.loc[co2_data["iso_code"] == "GTM"]
blz_co2 = co2_data.loc[co2_data["iso_code"] == "BLZ"]
mex_co2 = co2_data.loc[co2_data["iso_code"] == "MEX"]


pan_cum_co2_graph = px.line(
    pan_co2, x="year", y="cumulative_co2",
    labels=dict(
        year="Year", 
        cumulative_co2="Cumulative million tonnes of CO2 since 1949"
        ),
    line_shape="spline"
    )

pan_cum_co2_graph.update_layout(
    title={
        'text': "Cumulative CO2 emissions from Panama",
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
        },
    xaxis_title="Year",
    yaxis_title="Million tonnes of CO2",
)


app.layout = html.Div([
    html.Div([
        # header
    ], className='app__header'),

    html.Br(),

    html.Div([
        # body
        html.Div([
            # Panama: all graphs
            
            html.Div([
                # Panama: Annual CO2 graph with regression

                dcc.Graph(
                    id='pan-co2-reg',
                    figure={}
                ),

                dcc.Slider(
                    min=2021,
                    max=2050,
                    step=1,
                    value=2050,
                    marks={'2021': '2021', '2030': '2030', '2040': '2040', '2050': '2050'},
                    id='pan-co2-reg-year'
                )

            ], className='pan__co2__reg__container'),

            html.Br(),

            html.Div([
                # Panama: Cumulative CO2 graph

                dcc.Graph(
                    id='pan-cum-co2',
                    figure=pan_cum_co2_graph
                )

            ], className='pan__cum__co2__container'),

            html.Br(),

            html.Div([
               # Panama: Annual and cumulative decomposition of CO2 emissions
               # in cement, coal,and oil
               
               dcc.Graph(id='pan-decom-co2'),

                dcc.RadioItems(
                    ['Annual', 'Cumulative'],
                    value='Annual',
                    id='pan-decom-co2-graph-mode',
                    inline=True
                )

            ], className='pan__decom__co2__container'),
        ], className='pan__graphs__container'),

        html.Br(),

        html.Div([
            # Central America: all graphs

            html.Div([
                # Central America: Annual and cumulative CO2 graph

                dcc.Graph(id='cen-am-co2'),

                dcc.RadioItems(
                    ['Annual', 'Cumulative'],
                    value='Annual',
                    id='cen-am-co2-graph-mode',
                    inline=True
                )

            ], className='cen__am__co2__container'),

            html.Div([
                # Central America: Annual CO2 per capita graph

                dcc.Graph(id='cen-am-co2-per-cap'),

                dcc.RadioItems(
                    ['Annual', 'Cumulative'],
                    value='Annual',
                    id='cen-am-co2-per-cap-graph-mode',
                    inline=True
                )

            ], className='cen__am__co2__per__cap__container')

            
        ], className='cen__am__graphs__container')

    ], className='app__content')

], className='app__container')


def adjust_mode(data_field, graph_mode):
    """
    Helper function for adjusting data fields in cases based on whether
    user input is annual or cumulative.
    """

    if graph_mode not in {"Annual", "Cumulative"}:
        raise ValueError("graph_mode must be \"Annual or Cumulative\"")
    
    elif graph_mode == "Annual":
        return data_field

    return "".join(("cumulative_", data_field))


@app.callback(
    Output('pan-co2-reg', 'figure'),
    Input('pan-co2-reg-year', 'value')
)
def update_pan_co2_reg(input_year):
    pass


@app.callback(
    Output('pan-decom-co2', 'figure'),
    Input('pan-decom-co2-graph-mode', 'value')
)
def update_pan_decom_co2(graph_mode):
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"], y=pan_co2[adjust_mode("cement_co2", graph_mode)],
            mode="lines", name="Cement", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"], 
            y=pan_co2[adjust_mode("coal_co2", graph_mode)].interpolate(method="quadratic"),
            mode="lines", name="Coal (approximated)", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"], y=pan_co2[adjust_mode("oil_co2", graph_mode)],
            mode="lines", name="Oil", line_shape="spline"))
    
    fig.update_layout(
        title={
            'text': "CO2 emissions from Panama, coming from cement, coal, and oil",
            'x': 0.44,
            'y': 0.9,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Year",
        yaxis_title="Million tonnes of CO2",
    )

    return fig


@app.callback(
    Output('cen-am-co2', 'figure'),
    Input('cen-am-co2-graph-mode', 'value')
)
def update_cen_am_co2(graph_mode):
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"], y=pan_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Panama", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=cri_co2["year"], y=cri_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Costa Rica", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=nic_co2["year"], y=nic_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Nicaragua", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=hnd_co2["year"], y=hnd_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Honduras", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=slv_co2["year"], y=slv_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="El Salvador", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=gtm_co2["year"], y=gtm_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Guatemala", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=blz_co2["year"], y=blz_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Belize", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=mex_co2["year"], y=mex_co2[adjust_mode("co2", graph_mode)],
            mode="lines", name="Mexico", line_shape="spline"))

    fig.update_layout(
        title={
            'text': "CO2 emissions from Central American countries",
            'x':0.5,
            'y':0.9,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Year",
        yaxis_title="Million tonnes of CO2",
    )

    return fig


@app.callback(
    Output('cen-am-co2-per-cap', 'figure'),
    Input('cen-am-co2-per-cap-graph-mode', 'value')
)
def update_cen_am_co2_per_cap(graph_mode):
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"], 
            y=pan_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Panama", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=cri_co2["year"], 
            y=cri_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Costa Rica", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=nic_co2["year"], 
            y=nic_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Nicaragua", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=hnd_co2["year"], 
            y=hnd_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Honduras", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=slv_co2["year"], 
            y=slv_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="El Salvador", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=gtm_co2["year"], 
            y=gtm_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Guatemala", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=blz_co2["year"], 
            y=blz_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Belize", line_shape="spline"))
    fig.add_trace(
        go.Scatter(
            x=mex_co2["year"], 
            y=mex_co2[adjust_mode("co2_per_capita", graph_mode)],
            mode="lines", name="Mexico", line_shape="spline"))

    fig.update_layout(
        title={
            'text': "CO2 emissions from Central American countries",
            'x':0.5,
            'y':0.9,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Year",
        yaxis_title="Million tonnes of CO2",
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)