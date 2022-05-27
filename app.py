from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)

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
                    figure={}
                )

            ], className='pan__cum__co2__container'),

            html.Br(),

            html.Div([
               # Panama: Annual and cumulative decomposition of CO2 emissions
               # in cement, coal,and oil
               
               dcc.Graph(
                    id='pan-decom-co2',
                    figure={}
                ),

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

                dcc.Graph(
                    id='cen-am-co2',
                    figure={}
                ),

                dcc.RadioItems(
                    ['Annual', 'Cumulative'],
                    value='Annual',
                    id='cen-am-co2-graph-mode',
                    inline=True
                )

            ], className='cen__am__co2__container'),

            html.Div([
                # Central America: Annual CO2 per capita graph

                dcc.Graph(
                    id='cen-am-co2-per-cap',
                    figure={}
                ),

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
    pass


@app.callback(
    Output('cen-am-co2', 'figure'),
    Input('cen-am-co2-graph-mode', 'value')
)
def update_cen_am_co2(graph_mode):
    pass


@app.callback(
    Output('cen-am-co2-per-cap', 'figure'),
    Input('cen-am-co2-per-cap-graph-mode', 'value')
)
def update_cen_am_co2_per_cap(graph_mode):
    pass


if __name__ == '__main__':
    app.run_server(debug=True)