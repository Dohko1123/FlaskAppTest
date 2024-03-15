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

column_exceptions = {
    "bubble_chart": ["awaq_date", "awaq_common_name", "awaq_family"],
    "trendline_chart": ["awaq_date"]
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/bar_chart', methods=['GET'])
def bar_chart():
    params = request.args
    measure = params['column']
    x_axis = params['column']
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
    dimesion = params['column']

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)

    pie_chart = graphics.Pie_chart(dimesion)
    graphJSON = pie_chart.create_chart(df, 'Penguin by {}'.format(params['column']))
    header="Grafica de pastel"
    description = ""
    return render_template('graphic.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/heat_map', methods=['GET'])
def heat_map():
    longitude = 'awaq_longitude'
    latitude = 'awaq_latitude'
    describer = 'awaq_id'

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
    date = 'awaq_date'
    id = 'awaq_common_name'
    desc1 = params["column"]
    desc2 = 'awaq_family'  

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
    date = 'awaq_date'
    id = params["column"]

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
    elif params["id"] in column_exceptions.keys():
        return Response(mimetype="application/json", response=json.dumps({"code": "success", "columns": [column for column in columns if column not in column_exceptions[params["id"]]]}), status=200)
    return Response(mimetype="application/json", response=json.dumps({"code": "success", "columns": columns}), status=200)

@app.errorhandler(NotFound)
def handle_exception(e):
    return render_template('404.html'), 404