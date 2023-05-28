import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

dataset = pd.read_excel('TFL Bus Safety.xlsx')

dataset.drop_duplicates(inplace = True)

gender_incidents = dataset.groupby(by = 'Victims Sex').count().iloc[:, 7]

fig1 = px.bar(x = gender_incidents.index, y = gender_incidents, text_auto = '.f')
fig1.update_traces(marker_color='#3366CC', marker_line_color='black')
fig1.update_traces(textfont_size=14, textposition="outside", cliponaxis=False)
fig1.update_yaxes(showticklabels=False, visible = False)
fig1.update_xaxes(title = '', tickfont=dict(size=14))
fig1.update_layout(template = 'plotly_dark')
fig1.update_traces(width=.6)

age_group = dataset['Victims Age'].value_counts()

adult_group = age_group[0]
others = 0

for group in age_group[1:]:
    
    others += group

age_group = {'Adult': adult_group, 'Others': others}

fig2 = px.pie(age_group.keys(), values = age_group.values(), names = age_group.keys(), 
             color = age_group.keys(), #title = 'Incidents by age group',
             color_discrete_map={'Adult':'darkblue',
                                 'Others':'rgb(204, 204, 204)'})
fig2.update_traces(textposition='inside', textinfo='percent+label', textfont = {'color':'white'})
fig2.update_layout(font = dict(size = 16, color = 'white'))

fig2.update_layout(template = 'plotly_dark')
fig2.update_layout(showlegend=False)

event_type = round(dataset['Incident Event Type'].value_counts(normalize = True)*100, 2).sort_values()

fig3 = go.Figure(go.Bar(
    x=event_type.values,
    y= event_type.index,
    yaxis='y2',
    orientation='h',
    text=[f'{i}%' for i in event_type.values]
    ))
fig3.update_traces(marker_color='#3366CC', marker_line_color='black')
fig3.update_traces(textfont_size=12, textposition="outside", cliponaxis=False)
#fig3.update_layout(title_text='Percentage of incidents by Event Type')
fig3.update_layout(xaxis=dict(domain=[0.19, 0.9]),
                  yaxis2=dict(anchor='free', position=0.01,
                             side='right'))
fig3.update_xaxes(showticklabels=False, visible = False)
fig3.update_yaxes(tickfont=dict(size=11))
fig3.update_layout(template = 'plotly_dark')

monthly_incidents = pd.DataFrame()

for year in dataset.Year.unique():
    temp = dataset[dataset.Year == year]['Date Of Incident'].value_counts()

    temp = temp.to_frame()

    temp.reset_index(inplace=True)

    temp.sort_values(by='index', inplace=True)

    temp.rename(columns={'Date Of Incident': 'Incidents'}, inplace=True)

    monthly_incidents = pd.concat([monthly_incidents, temp], axis=0)

    monthly_incidents.reset_index(inplace=True, drop=True)

monthly_incidents.rename(columns={'index': 'Period'}, inplace=True)

fig4 = px.line(monthly_incidents, x='Period', y='Incidents', #title='Evolution of monthly incidents',
               markers=True)

fig4.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig4.add_hline(y=monthly_incidents.Incidents.mean(), line_width=1, line_dash="dash", line_color="red",
              annotation_text="Average of incidents", annotation_position="top left")
fig4.update_traces(marker_color='#3366CC', marker_line_color='black')
fig4.update_layout(template = 'plotly_dark')
fig4.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False})
fig4.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))

collision_incident = dataset[(dataset['Incident Event Type'] == 'Collision Incident') & (dataset['Victims Sex'] == 'Female')]

collision_grouped = collision_incident.groupby(by='Date Of Incident')['Year'].count()

collision_index = collision_grouped.index[collision_grouped == collision_grouped.max()]

index_number = 0

for index in collision_grouped.index:

    if index != collision_index:

        index_number += 1

    else:

        break

color_discrete_sequence = ['#3366CC'] * collision_incident['Date Of Incident'].value_counts().count()
color_discrete_sequence[index_number] = 'red'

fig5 = px.histogram(collision_incident, x='Date Of Incident', #title = 'Monthly collision incidents among female victims',
                   nbins = 50,)
fig5.update_layout(bargap=0.2)
fig5.update_traces(marker_color=color_discrete_sequence, marker_line_color='black')
fig5.update_layout(template = 'plotly_dark')
fig5.update_xaxes(title = '', tickfont=dict(size=12))
fig5.update_yaxes(title = 'Number of incidents', tickfont=dict(size=12))
fig5.add_annotation(x= collision_index[0], y=collision_grouped.max(),
            text= f"Max number on {collision_index[0].strftime('%B/%Y')}",
            showarrow=False,
            yshift = 15)
fig5.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False})

child_victims = dataset[dataset['Victims Age'] == 'Child']

avg_child = child_victims.groupby(by = 'Date Of Incident')['Year'].count()

avg_child.index = avg_child.index.strftime('%b/%Y')

fig6 = px.histogram(child_victims, x='Date Of Incident', nbins = 50, #title = 'Monthly incidents among child victims',
                   opacity = 0.30)

fig6 = px.histogram(child_victims, x='Date Of Incident', nbins = 50, #title = 'Monthly incidents among child victims',
                   opacity = 0.40)

fig6.update_layout(bargap=0.2)
fig6.update_layout(template = 'plotly_dark')
fig6.update_xaxes(title = '', tickfont=dict(size=12))
fig6.update_yaxes(title = 'Number of incidents', tickfont=dict(size=12))
fig6.add_hline(y=avg_child.mean(), line_width=4, line_dash="dash", line_color="red")
fig6.add_annotation(x= '2015-07-01', y=avg_child.mean(),
            text= f"Average of incidents: {round(avg_child.mean(), 1)}",
            showarrow=False,
            yshift = 15)
fig6.update_traces(marker_color= '#3366CC', marker_line_color='black')
fig6.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False})

treated_onscene = dataset[dataset['Injury Result Description'] == 'Injuries treated on scene']
treated_onscene = treated_onscene[(treated_onscene['Victims Sex'] == 'Female') | (treated_onscene['Victims Sex'] == 'Male')]

injuries_male = treated_onscene[treated_onscene['Victims Sex'] == 'Male'].shape[0]

injuries_female = treated_onscene[treated_onscene['Victims Sex'] == 'Female'].shape[0]

total_injuries = pd.DataFrame(data = [{'Injuries': injuries_male, 'Gender': 'Male'},
                                {'Injuries': injuries_female, 'Gender': 'Female'}])
total_injuries['aux'] = 0

fig7 = px.bar(total_injuries, x = 'aux', y="Injuries",  color="Gender", text_auto=True, width = 500, height = 500,
            color_discrete_map = {'Male': '#3366CC', 'Female': 'red'})
fig7.update_xaxes(showticklabels=False, title=None)
fig7.update_yaxes(showticklabels=False, title=None)
fig7.update_traces(width=.4)
fig7.add_hline(y= total_injuries.Injuries.sum(), line_width=1, line_dash="dash", line_color="black",
              annotation=dict(font_size=16, font_family="Arial"),
              annotation_text=f"Total {total_injuries.Injuries.sum()}", annotation_position="top left")
fig7.update_layout(template = 'plotly_dark')
fig7.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False})

elderly_victims = dataset[(dataset['Victims Age'] == 'Elderly') & (dataset['Year'] == 2017)]

incidents_elderly = elderly_victims['Date Of Incident'].value_counts().sort_index()

index_max = incidents_elderly.index[incidents_elderly == incidents_elderly.max()]

index_number = 0

for index in incidents_elderly.index:

    if index != index_max:

        index_number += 1

    else:

        break

color_discrete_sequence = ['#3366CC'] * incidents_elderly.count()
color_discrete_sequence[index_number] = 'red'

fig8 = px.line(incidents_elderly, y=incidents_elderly.values, #title ='2017 monthly incidents among elderly victims',
              text = incidents_elderly.index.strftime('%b %Y'))
fig8.update_traces(textposition = ['top center', 'bottom right', 'top center', 'top right', 'bottom left', 'bottom center',
                                  'top center', 'bottom center', 'top center', 'bottom center', 'top center', 'bottom center'])
fig8.update_traces(marker_color=color_discrete_sequence, marker_line_color='black',
                  textfont_color = ['red' if i == index_max else 'white' for i in incidents_elderly.index],
                  textfont_size = [16 if i == index_max else 12 for i in incidents_elderly.index],
                  marker_size = [12 if i == index_max else 5 for i in incidents_elderly.index])
fig8.update_layout(template = 'plotly_dark')
fig8.update_xaxes(showticklabels=False, visible = False)
fig8.update_yaxes(title = 'Number of incidents', tickfont=dict(size=12))
fig8.update_layout(yaxis_range=[50,90])
fig8.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False})

operator = dataset.groupby(by='Operator')['Date Of Incident'].value_counts()
operator = operator.to_frame()
operator.rename(columns = {'Date Of Incident': 'Number of Incidents'}, inplace = True)
operator = operator.sort_index()
operator = operator.reset_index(level=[0, 1])

mask = operator.Operator.value_counts() > 3

list_filter = []

for index, value in zip(mask.index, mask.values):

    if value:
        list_filter.append(index)

operator = operator[operator.Operator.isin(list_filter)]

fig9 = px.line(operator, x="Date Of Incident", y="Number of Incidents", animation_frame="Operator",
           range_x=[operator['Date Of Incident'].min(), operator['Date Of Incident'].max()],
                 range_y=[-19, operator['Number of Incidents'].max()], #title='Distribution of incidents over time by operator',
                 markers = True,)

fig9.update_layout(template = 'plotly_dark')
fig9.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 3000
fig9.update_xaxes(title = '')
fig9.update_yaxes(title = 'Number of incidents', tickfont=dict(size=12))
fig9.update_traces(marker_color='#3366CC', marker_line_color='black')
fig9.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False})

cyclists = dataset[dataset['Victim Category'] == 'Cyclist']

incidents_cyclists = cyclists['Incident Event Type'].value_counts()

collision_incident = incidents_cyclists[0]
others = 0

for event in incidents_cyclists[1:]:
    others += event

incidents_cyclists = {'Collision Incident': collision_incident, 'Others': others}

fig10 = px.pie(incidents_cyclists.keys(), values = incidents_cyclists.values(), names = incidents_cyclists.keys(),
             color = incidents_cyclists.keys(), #title = 'Most common incident event type among cyclists',
             color_discrete_map={'Collision Incident':'darkblue',
                                 'Others':'rgb(204, 204, 204)'})
fig10.update_traces(textposition='inside', textinfo='percent+label', textfont = {'color':'white'})
fig10.update_layout(font = dict(size = 16, color = 'black'))
fig10.update_layout(showlegend=False)
fig10.update_layout(template = 'plotly_dark')

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div( style={'backgroundColor': 'black'},
    children=[
        html.H1('Risk Analysis in London Public Transport',
                style={'font-size': '38px', 'textAlign': 'center', 'color': 'white'}),

        html.Div([
            html.Div([
                html.H3('What is the percentage of incidents by Event Type?',
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig3)
            ], style={'width': '70%', 'display': 'inline-block'}),
            html.Div([
                html.H3('Which Age Group was more involved in incidents?',
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig2)
            ], style={'width': '30%', 'display': 'inline-block'}),
        ], className='plot-row'),

        html.Div([
            html.Div([
                html.H3('How is the evolution of monthly incidents over time?',
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig4)
            ], style={'width': '60%', 'display': 'inline-block'}),
            html.Div([
                html.H3('What is the number of incidents by Gender?',
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig1)
            ], style={'width': '40%', 'display': 'inline-block'}),

        ], className='plot-row'),

        html.Div([
            html.Div([
                html.H3(
                    "When the incident type was Collision, in which month was there the biggest number of incidents with female victims?",
                    style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig5)
            ], style={'width': '60%', 'display': 'inline-block'}),
            html.Div([
                html.H3("What is the Incident Type most common between Cyclists?",
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig10)
            ], style={'width': '40%', 'display': 'inline-block'}),
        ], className='plot-row'),

        html.Div([
            html.Div([
                html.H3("Considering the Operator, what is the distribution of incidents over time?",
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig9)
            ], style={'width': '60%', 'display': 'inline-block'}),
            html.Div([
                html.H3(
                    "Considering the injury result description as Treated on Scene, what is the total number of incidents by gender?",
                    style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig7)
            ], style={'width': '40%', 'display': 'inline-block'}),

        ], className='plot-row'),

        html.Div([
            html.Div([
                html.H3('In which month of 2017 was there the highest number of incidents with Elderly victims?',
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig8)
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.H3('What was the average of incidents by month with Child victims?',
                        style={'font-size': '20px', 'font-weight': 'normal', 'color': 'white'}),
                dcc.Graph(figure=fig6)
            ], style={'width': '50%', 'display': 'inline-block'}),

        ], className='plot-row'),

    ])

if __name__ == '__main__':
    app.run_server(debug=True)
