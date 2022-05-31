from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import pickle


### Setup ###

app = Dash(__name__)

app.title = "Panama and Central America CO2 visualization"
server = app.server


co2_data = pd.read_csv("owid-co2-data.csv")

pan_co2 = co2_data.loc[co2_data["iso_code"] == "PAN"]
cri_co2 = co2_data.loc[co2_data["iso_code"] == "CRI"]
nic_co2 = co2_data.loc[co2_data["iso_code"] == "NIC"]
hnd_co2 = co2_data.loc[co2_data["iso_code"] == "HND"]
slv_co2 = co2_data.loc[co2_data["iso_code"] == "SLV"]
gtm_co2 = co2_data.loc[co2_data["iso_code"] == "GTM"]
blz_co2 = co2_data.loc[co2_data["iso_code"] == "BLZ"]
mex_co2 = co2_data.loc[co2_data["iso_code"] == "MEX"]


with open("pan_co2_linear_model.pkl", "rb") as linear_model_file:
    co2_linreg = pickle.load(linear_model_file)


### Static graphs ###

pan_cum_co2_graph = px.line(
    pan_co2,
    x="year",
    y="cumulative_co2",
    labels=dict(
        year="Year", cumulative_co2="Cumulative million tonnes of CO2 since 1949"
    ),
    line_shape="spline",
)

pan_cum_co2_graph.update_layout(
    title={
        "text": "Cumulative CO2 emissions from Panama",
        "x": 0.5,
        "y": 0.95,
        "xanchor": "center",
        "yanchor": "top",
    },
    xaxis_title="Year",
    yaxis_title="Million tonnes of CO2",
    font_family="DM Sans",
)

cen_am_co2_per_cap_graph = go.Figure()

cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=pan_co2["year"],
        y=pan_co2["co2_per_capita"],
        mode="lines",
        name="Panama",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=cri_co2["year"],
        y=cri_co2["co2_per_capita"],
        mode="lines",
        name="Costa Rica",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=nic_co2["year"],
        y=nic_co2["co2_per_capita"],
        mode="lines",
        name="Nicaragua",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=hnd_co2["year"],
        y=hnd_co2["co2_per_capita"],
        mode="lines",
        name="Honduras",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=slv_co2["year"],
        y=slv_co2["co2_per_capita"],
        mode="lines",
        name="El Salvador",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=gtm_co2["year"],
        y=gtm_co2["co2_per_capita"],
        mode="lines",
        name="Guatemala",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=blz_co2["year"],
        y=blz_co2["co2_per_capita"],
        mode="lines",
        name="Belize",
        line_shape="spline",
    )
)
cen_am_co2_per_cap_graph.add_trace(
    go.Scatter(
        x=mex_co2["year"],
        y=mex_co2["co2_per_capita"],
        mode="lines",
        name="Mexico",
        line_shape="spline",
    )
)

cen_am_co2_per_cap_graph.update_layout(
    title={
        "text": "CO2 per capita emissions from Central American countries",
        "x": 0.5,
        "y": 0.9,
        "xanchor": "center",
        "yanchor": "top",
    },
    xaxis_title="Year",
    yaxis_title="CO2 tonnes per person",
    font_family="DM Sans",
)


### Layout ###

app.layout = html.Div(
    [
        html.Div(
            [
                # header
                html.H1(
                    "CO2 emissions in Panama and Central America",
                    className="app__header__title",
                ),
                html.P(
                    "This data was extracted from the Our World in Data organization [1].",
                    className="app__header__desc",
                ),
            ],
            className="app__header",
        ),
        html.Hr(),
        html.Div(
            [
                # body
                html.H2("Data for Panama", className="pan__co2__header"),
                html.Div(
                    [
                        # Panama: all graphs
                        html.Div(
                            [
                                # Panama: Annual CO2 graph with regression
                                dcc.Graph(id="pan-co2-reg"),
                                dcc.Slider(
                                    min=2021,
                                    max=2050,
                                    step=1,
                                    value=2050,
                                    marks={
                                        str(year): str(year)
                                        for year in range(2021, 2051, 5)
                                    },
                                    id="pan-co2-reg-year",
                                ),
                            ],
                            className="pan__co2__reg__container",
                        ),
                        html.Br(),
                        html.Div(
                            [
                                # Panama: Cumulative CO2 graph
                                dcc.Graph(id="pan-cum-co2", figure=pan_cum_co2_graph)
                            ],
                            className="pan__cum__co2__container",
                        ),
                        html.Br(),
                        html.Div(
                            [
                                # Panama: Annual and cumulative decomposition of CO2 emissions
                                # in cement, coal,and oil
                                dcc.Graph(id="pan-decom-co2"),
                                dcc.RadioItems(
                                    ["Annual", "Cumulative"],
                                    value="Annual",
                                    id="pan-decom-co2-graph-mode",
                                    inline=True,
                                ),
                            ],
                            className="pan__decom__co2__container",
                        ),
                    ],
                    className="pan__graphs__container",
                ),
                html.Hr(),
                html.H2("Data for Central America", className="cen__am__co2__header"),
                html.Div(
                    [
                        # Central America: all graphs
                        html.Div(
                            [
                                # Central America: Annual and cumulative CO2 graph
                                dcc.Graph(id="cen-am-co2"),
                                dcc.RadioItems(
                                    ["Annual", "Cumulative"],
                                    value="Annual",
                                    id="cen-am-co2-graph-mode",
                                    inline=True,
                                ),
                            ],
                            className="cen__am__co2__container",
                        ),
                        html.Div(
                            [
                                # Central America: Annual CO2 per capita graph
                                dcc.Graph(
                                    id="cen-am-co2-per-cap",
                                    figure=cen_am_co2_per_cap_graph,
                                ),
                            ],
                            className="cen__am__co2__per__cap__container",
                        ),
                    ],
                    className="cen__am__graphs__container",
                ),
                html.Hr(),
                html.Cite(
                    "[1] Hannah Ritchie, Max Roser and Pablo Rosado (2020) - \"CO₂ and Greenhouse Gas Emissions\". Published online at OurWorldInData.org. Retrieved from: 'https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions' [Online Resource]",
                    className="source__cite",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)


### Helpers and callbacks ###


def adjust_mode(data_field, graph_mode):
    """
    Helper function for adjusting data fields in cases based on whether
    user input is annual or cumulative.
    """

    if graph_mode not in {"Annual", "Cumulative"}:
        raise ValueError('graph_mode must be "Annual or Cumulative"')

    elif graph_mode == "Annual":
        return data_field

    return "".join(("cumulative_", data_field))


@app.callback(Output("pan-co2-reg", "figure"), Input("pan-co2-reg-year", "value"))
def update_pan_co2_reg(input_year):

    year_proy = np.arange(2021, input_year + 1)
    co2_proy = co2_linreg.predict(
        np.arange(2021, input_year + 1).reshape(input_year - 2020, 1)
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"],
            y=pan_co2["co2"],
            mode="lines+markers",
            name="Current data",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=year_proy,
            y=co2_proy,
            mode="lines+markers",
            name="Proyected data",
            line_shape="spline",
        )
    )

    fig.update_layout(
        title={
            "text": "Predictions for annual CO2 emissions from Panama",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis_title="Year",
        yaxis_title="Million tonnes of CO2",
        font_family="DM Sans",
    )

    return fig


@app.callback(
    Output("pan-decom-co2", "figure"), Input("pan-decom-co2-graph-mode", "value")
)
def update_pan_decom_co2(graph_mode):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"],
            y=pan_co2[adjust_mode("cement_co2", graph_mode)],
            mode="lines",
            name="Cement",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"],
            y=pan_co2[adjust_mode("coal_co2", graph_mode)].interpolate(
                method="quadratic"
            ),
            mode="lines",
            name="Coal (approximated)",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"],
            y=pan_co2[adjust_mode("oil_co2", graph_mode)],
            mode="lines",
            name="Oil",
            line_shape="spline",
        )
    )

    fig.update_layout(
        title={
            "text": "CO2 emissions from Panama, coming from cement, coal, and oil",
            "x": 0.44,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis_title="Year",
        yaxis_title="Million tonnes of CO2",
        font_family="DM Sans",
    )

    return fig


@app.callback(Output("cen-am-co2", "figure"), Input("cen-am-co2-graph-mode", "value"))
def update_cen_am_co2(graph_mode):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=pan_co2["year"],
            y=pan_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Panama",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=cri_co2["year"],
            y=cri_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Costa Rica",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=nic_co2["year"],
            y=nic_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Nicaragua",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=hnd_co2["year"],
            y=hnd_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Honduras",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=slv_co2["year"],
            y=slv_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="El Salvador",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gtm_co2["year"],
            y=gtm_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Guatemala",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=blz_co2["year"],
            y=blz_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Belize",
            line_shape="spline",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=mex_co2["year"],
            y=mex_co2[adjust_mode("co2", graph_mode)],
            mode="lines",
            name="Mexico",
            line_shape="spline",
        )
    )

    fig.update_layout(
        title={
            "text": "CO2 emissions from Central American countries",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis_title="Year",
        yaxis_title="Million tonnes of CO2",
        font_family="DM Sans",
    )

    return fig


### Run app ###

if __name__ == "__main__":
    app.run(debug=True)
