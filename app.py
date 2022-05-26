from dash import Dash, html, dcc

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
                )
            ], className='cen__am__co2__container'),

            html.Div([
                # Central America: Annual CO2 per capita graph

                dcc.Graph(
                    id='cen-am-co2-per-cap',
                    figure={}
                )
            ], className='cen__am__co2__per__cap__container')

            
        ], className='cen__am__graphs__container')

    ], className='app__content')

], className='app__container')


if __name__ == '__main__':
    app.run_server(debug=True)