from flask import Flask, request, jsonify, render_template, Response
from werkzeug.exceptions import NotFound
import json
import pandas as pd
import numpy as np
import connection
import graphics

app = Flask(__name__)

conn = connection.first_connection()
cursor = connection.get_cursor(conn)
table_name = 'awaq'
columns = connection.get_colums_names(cursor, table_name)

cols_required = {
    "bar_chart": ["Column"],
    "pie_chart": ["Column"],
    "heat_map": ["Longitude", "Latitude", "Describer"],
    "bubble_chart": ["Date", "Column", "Describer 1", "Describer 2"],
    "trendline_chart": ["Date", "Column"]
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/bar_chart', methods=['GET'])
def bar_chart():
    params = request.args
    measure = params['column1']
    x_axis = params['column1']
    y_axis = 'Cantidad'
    function = pd.Series
    color = 'blue'

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    for i in data[1]:
        print(i)
    df = pd.DataFrame(data, columns=columns)
    bar_chart = graphics.Bar_chart(measure, x_axis, y_axis, function, color)
    graphJSON= bar_chart.create_chart(df)
    header="Grafica de Barras"
    description = ""
    return render_template('graphic.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/pie_chart', methods=['GET'])
def pie_chart():
    params = request.args
    dimesion = params['column1']

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)

    pie_chart = graphics.Pie_chart(dimesion)
    graphJSON = pie_chart.create_chart(df, 'Penguin by {}'.format(params['column1']))
    header="Grafica de pastel"
    description = ""
    return render_template('graphic.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/heat_map', methods=['GET'])
def heat_map():
    params = request.args
    longitude = params["column1"]
    latitude = params["column2"]
    describer = params["column3"]

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    
    geo_chart = graphics.Geo_chart(latitude, longitude, describer)
    graphJSON = geo_chart.create_chart(df, 'Mapa de calor')
    header="Mapa de calor"
    description = ""
    return render_template('graphic.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/bubble_chart', methods=['GET'])
def bubble_chart():
    params = request.args
    date = params["column1"]
    id = params["column2"]
    desc1 = params["column3"]
    desc2 = params["column4"]

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    print(df)

    bubble_chart = graphics.Bubble_chart(id,date, desc1, desc2)
    graphJSON = bubble_chart.create_chart(df, 'Mapa de burbujas')
    header="Mapa de burbujas"
    description = ""
    return render_template('graphic.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/trendline_chart', methods=['GET'])
def trendline_chart():
    params = request.args
    date = params["column1"]
    id = params["column2"]

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    print(df)

    trendline_chart = graphics.Trendline_chart(id,date)
    graphJSON = trendline_chart.create_chart(df, 'Mapa de tendencia')
    header="Mapa de tendencia"
    description = ""
    return render_template('graphic.html', graphJSON=graphJSON, header=header,description=description)


@app.route('/var_getter', methods=['GET'])
def var_getter():
    params = request.args
    if not columns:
        return Response(mimetype="application/json", response=json.dumps({"code": "error", "details": "The data was not found on the server."}), status=404)
    return Response(mimetype="application/json", response=json.dumps({"code": "success", "columns": columns, "required": cols_required[params["id"]]}), status=200)

@app.errorhandler(NotFound)
def handle_exception(e):
    return render_template('404.html'), 404