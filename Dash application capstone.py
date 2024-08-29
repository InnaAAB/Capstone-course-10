# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#get a list of all the launch sites - ON HOLD

#launchList = spacex_df['Launch Site'].unique()


# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
                                        
                                        #TASK 1
                                        html.Div(dcc.Dropdown(id='site-dropdown',
                                                              options=[{'label': 'All', 'value': 'ALL'},
                                                                       {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                       {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                                       {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                       {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                                            value='ALL',
                                                            placeholder="Select Site",
                                                            searchable=True
                                        )),
                                        html.Br(),

                                        #TASK 2
                                        html.Div(dcc.Graph(id='success-pie-chart')),
                                        html.Br(),

                                        #TASK 3
                                        html.P("Payload range (Kg):"),
                                        html.Div(dcc.RangeSlider(
                                            id='payload-slider',
                                            min=0,max=10000,step=100,
                                            marks={0:'0', 100: '100'},
                                            value=[max_payload,500]
                                        )),

                                        #TASK 4
                                        html.Div(dcc.Graph(
                                            id='success-payload-scatter-chart'))
                                        ])


#TASK 2
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # recession_data = data[data['Recession'] == 1]
    #filtered_df = spacex_df

    if entered_site == 'ALL':
        fig = px.pie(data_frame=spacex_df, values='class', 
        names='Launch Site', 
        title='successful launches for all sites')
        return fig
        
    else:
        # return the outcomes piechart for a selected site
        HolDT = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = HolDT.groupby('class')['Launch Site'].value_counts().reset_index()

        fig = px.pie(data_frame=filtered_df , values='count', 
        names='class', 
        title='successful launches for ' + entered_site)
        return fig

#,payload_masskg
#TASK 4
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')])
def get_payload_scatter_chart(entered_site,value): 
    #get min and max values from the slider 
    #payload_masskg
    min_selpayM, max_selpayM = value
    if entered_site == "ALL":
        Filtpaymas = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_selpayM) & (spacex_df['Payload Mass (kg)'] <= max_selpayM)]
        fig = px.scatter(data_frame=Filtpaymas, x='Payload Mass (kg)',y='class',color='Booster Version Category',
                            title="success by payload mass(kg)")
        return fig
    else:
        HopayMas = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] >= min_selpayM) & (spacex_df['Payload Mass (kg)'] <= max_selpayM)]
        fig = px.scatter(data_frame= HopayMas, x='Payload Mass (kg)',y='class',color='Booster Version Category',
                         title="success by payload mass(kg) for " + entered_site)
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()

