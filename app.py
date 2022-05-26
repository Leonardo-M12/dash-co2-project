from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        # header
    ]),

    html.Br(),

    html.Div([
        # body
        html.Div([
            # Panama: all graphs
            
            html.Div([
            # Panama: Annual CO2 graph with regression
            ]),

            html.Br(),

            html.Div([
                # Panama: Cumulative CO2 graph
            ]),

            html.Br(),

            html.Div([
               # Panama: Annual and cumulative decomposition of CO2 emissions
               # in cement, coal,and oil
            ]),
        ]),

        html.Br(),

        html.Div([
            # Central America: all graphs

            html.Div([
                # Central America: Annual and cumulative CO2 graph
            ]),

            html.Br(),

            html.Div([
                # Central America: Annual CO2 per capita graph
            ])

            
        ])

    ])

])


if __name__ == '__main__':
    app.run_server(debug=True)