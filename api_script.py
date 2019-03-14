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

    if min_length:
        query += ' duration>=' + str(min_length) + ' AND'

    if max_length:
        query += ' duration<=' + str(max_length) + ' AND'

    
    query = query[:-4] + ';'

    cnx = sqlite3.connect('/Users/christophermarker/Documents/BV_API_Project/bvde.db')
    cnx.row_factory = make_dicts
    cur = cnx.cursor()

    print(query)

    results = cur.execute(query).fetchall()

    return jsonify(results)

app.run()
