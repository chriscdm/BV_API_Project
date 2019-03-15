from flask import Flask, request, jsonify, g
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
import sqlite3
#import os

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Home</h1>"


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.route('/all_songs', methods=['GET'])
def api_all():
    cnx = sqlite3.connect('/Users/christophermarker/Documents/BV_API_Project/bvde.db')
    cnx.row_factory = make_dicts
    cur = cnx.cursor()
    all_songs = cur.execute('SELECT title,artist,name,duration FROM songs INNER JOIN genres ON songs.genre=genres.id;').fetchall()

    return jsonify(all_songs)

@app.route('/songs', methods=['GET'])
def api_filter():
    query_parameters = request.args

    artist = query_parameters.get('artist')
    song = query_parameters.get('song')
    genre = query_parameters.get('genre')
    min_length = query_parameters.get('min_length')
    max_length = query_parameters.get('max_length')

    query = 'SELECT title,artist,name,duration FROM songs INNER JOIN genres ON songs.genre=genres.id WHERE'

    if artist:
        query += ' artist=' + "'" + str(artist) + "'" + ' AND'
    
    if song:
        query += ' title=' + "'" + str(song) + "'" + ' AND'
    
    if genre:
        query += ' name=' + "'" + str(genre) + "'" + ' AND'

    def convert_time(i):
        units = i.split(':')
        units = [float(i) for i in units]

        if len(units) == 2:
            seconds = (units[0] * 60) + units[1]
        if len(units) == 3:
            seconds = (units[0] * 3600) + (units[1] * 60) + units[2]
        
        return seconds

    if min_length:
        try:
            if (type(int(min_length)) == int) == True or (type(int(min_length)) == float) == True:
                pass
        except:
            print('donkey')
            if len(min_length.split(':')) >= 2 and len(min_length.split(':')) <= 3:
                min_length = convert_time(min_length)
            else:
                pass
        query += ' duration>=' + str(min_length) + ' AND'

    if max_length:
        try:
            if (type(int(max_length)) == int) == True or (type(int(max_length)) == float) == True:
                pass
        except:
            if len(max_length.split(':')) >= 2 and len(max_length.split(':')) <= 3:
                max_length = convert_time(max_length)
            else:
                pass
        query += ' duration<=' + str(max_length) + ' AND'

    print(type(min_length))

    query = query[:-4] + ';'

    cnx = sqlite3.connect('/Users/christophermarker/Documents/BV_API_Project/bvde.db')
    cnx.row_factory = make_dicts
    cur = cnx.cursor()

    print(query)

    results = cur.execute(query).fetchall()

    return jsonify(results)

app.run()
