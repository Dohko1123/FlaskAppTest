import plotly
import plotly.express as px
import pandas as pd
import json

import plotly.graph_objects as go

class Bar_chart:
    def __init__(self, measure, x_axis, y_axis, function, color='blue'):
        self.measure = measure
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.function = function
        self.color = color

    def create_chart(self, df):
        value_counts = self.function(df[self.measure]).value_counts()
        fig = go.Figure()
        fig.add_trace(go.Bar(x = value_counts.index, y = value_counts, marker_color=self.color))
        fig.update_layout(title = self.measure, xaxis = dict(title=self.x_axis), yaxis = dict(title=self.y_axis))
        fig.update_yaxes(range=[0, max(value_counts)*1.1])
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
class Pie_chart:
    def __init__(self, tag):
        self.tag = tag

    def create_chart(self, df, title):
        # Count the occurrences of the tag in the dataframe
        df_count = df[self.tag].value_counts().reset_index()
        df_count.columns = [self.tag, 'count']

        fig = px.pie(df_count, values='count', names=self.tag, title=title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
class Geo_chart:
    def __init__(self, lat, lon, bird_id):
        self.lat = lat
        self.lon = lon
        self.bird_id = bird_id

    def create_chart(self, df, title):
        fig = go.Figure(data=go.Scattergeo(
            lon = df[self.lon],
            lat = df[self.lat],
            text = df[self.bird_id],
            mode = 'markers',
        ))

        fig.update_layout(title = title)

        fig.update_layout(
            title = title,
            autosize=True,
            height=500,
            geo=dict(
                center=dict(
                    lat=5.20830,
                    lon=-75.6667
                ),
                scope='south america',
                projection_scale=5
            )
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
class Bubble_chart:
    def __init__(self, group_columns, date_column, count_column, color_column):
        self.group_columns = group_columns
        self.date_column = date_column
        self.count_column = count_column
        self.color_column = color_column

    def create_chart(self, df, title):
        df_count2 = df.groupby([self.date_column , self.group_columns, self.count_column, self.color_column]).size().reset_index(name='counts')
        df_count2[self.date_column] = pd.to_datetime(df_count2[self.date_column], infer_datetime_format=True)
        print(df_count2)
        fig = px.scatter(df_count2,
                        x = self.date_column,
                        y = 'counts',
                        size = 'counts',
                        color=self.count_column)
        
        fig.update_layout(title = title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
        
class Trendline_chart:
    def __init__(self, group_columns, date_column):
        self.group_columns = group_columns
        self.date_column = date_column

    def create_chart(self, df, title):
        df_count = df.groupby([self.date_column, self.group_columns]).size().reset_index(name='counts')
        df_count[self.date_column] = pd.to_datetime(df_count[self.date_column], infer_datetime_format=True)

        fig = px.scatter(df_count, x=self.date_column, y='counts', trendline="ols")

        fig.update_layout(title = title)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON