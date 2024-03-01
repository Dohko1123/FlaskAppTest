from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np


df = pd.read_csv('penguins.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart1')
def chart1():
    value_counts = df['Breed Stage'].value_counts()

    fig = go.Figure()

    fig.add_trace(go.Bar(x = value_counts.index, y = value_counts))

    fig.update_layout(title = "Estado de crianza", xaxis = dict(title='Estado'), yaxis = dict(title='Cantidad'))

    fig.update_yaxes(range=[0, 10000])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafica de Barras"
    description = """
    Grafica de Barras que muestra el estado de crianza de los pinguinos.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart2')
def chart2():
    fig = px.pie(df, values='ArgosQuality', names='Sex', title='Argos Quality by Sex')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafica de pastel"
    description = """
    Grafica de pastel que muestra la calidad de Argos por sexo.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart3')
def chart3():
    df2= df.DateGMT.value_counts().reset_index().rename(columns={'index': 'DateGMT', 'DateGMT': 'count'})
    df2['DateGMT'] = pd.to_datetime(df2['DateGMT'], dayfirst=True)
    df2['year'] = pd.DatetimeIndex(df2['DateGMT']).year


    df2=df2.year.value_counts().reset_index().rename(
            columns={'index': 'year', 'year': 'count'})
    df2=df2.sort_values(by='year',ascending=True)
    fig = px.line(df2, x='year', y="count")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafica de Tendencia"
    description = """
    Grafica de tendencia que muestra la cantidad de pinguinos por año.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart4')
def chart4():
    df_count = df.groupby(['DateGMT', 'BirdId']).size().reset_index(name='counts')

    df_count['DateGMT'] = pd.to_datetime(df_count['DateGMT'], format="%d/%m/%Y")

    # Create a scatter plot
    fig = px.scatter(df_count, x='DateGMT', y='counts', trendline="ols")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafica de Linea Tendencia"
    description = """
    Grafica de tendencia que muestra la cantidad de pinguinos por fecha.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart5')
def chart5():
    df_count2 = df.groupby(['DateGMT', 'BirdId', 'Breed Stage', 'Sex']).size().reset_index(name='counts')
    df_count2['DateGMT'] = pd.to_datetime(df_count2['DateGMT'], format="%d/%m/%Y")

    fig = px.scatter(df_count2,
                    x = 'DateGMT',
                    y = 'counts',
                    size = 'counts',
                    color='Breed Stage')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafica de Burbujas"
    description = """
    Grafica de burbujas que muestra la cantidad de pinguinos por fecha y estado de crianza.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/chart6')
def chart6():
    fig = go.Figure(data=go.Scattergeo(
        lon = df['Longitude'],
        lat = df['Latitude'],
        text = df['BirdId'],
        mode = 'markers',
        ))

    fig.update_layout(
            title = 'Adelie penguin (Pygoscelis adeliae) telemetry',
        )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Grafica de Mapa de Calor"
    description = """
    Grafica de mapa de calor que muestra la ubicación de los pinguinos.
    """
    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)

if __name__ == '__main__':

    app.run(debug=True)