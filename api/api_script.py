from flask import Flask, request, jsonify, g
import sqlite3
import os
import sys

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():

    return "<h1>Basic Documentation</h1>" +\
        "<h3>An API to return data regarding BV's song database in JSON format</h3>" +\
        "<h3>Sample requests:</h3><h3>Request all songs</h3>" +\
        "<p>http://127.0.0.1:5000/all_songs</p><h3>Request genre information</h3>" +\
        "<p>http://127.0.0.1:5000/genres</p>"+\
        "<h3>Search for artist, song, genre, min duration, or max duration</h3>"+\
        "<p>http://127.0.0.1:5000/songs?artist=Bobby+Darin</p>"+\
        "<p>http://127.0.0.1:5000/songs?song=Physical</p>"+\
        "<p>http://127.0.0.1:5000/songs?genre=Pop </p>"+\
        "<p>http://127.0.0.1:5000/songs?min_length=194&max_length=196</p>"+\
        "<p>http://127.0.0.1:5000/songs?min_length=00:03:14&max_length=03:16</p>"

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/all_songs', methods=['GET'])
def api_all():
    cnx = sqlite3.connect('../data/bvde.db')
    cnx.row_factory = make_dicts
    cur = cnx.cursor()
    all_songs = cur.execute('SELECT title,artist,name AS "genre_name",duration AS' +\
         ' "duration_in_seconds" FROM songs INNER JOIN genres ON songs.genre=genres.id;').fetchall()

    return jsonify(all_songs)

@app.route('/songs', methods=['GET'])
def api_filter():
    query_parameters = request.args # retrieving the query parameters from the user - defining my query parameters as what has been supplied by the the user

    artist = query_parameters.get('artist') # extracting specific terms from the collection of query parameters
    song = query_parameters.get('song')
    genre = query_parameters.get('genre')
    min_length = query_parameters.get('min_length')
    max_length = query_parameters.get('max_length')

    query = 'SELECT title,artist,name AS "genre_name",duration as "duration_in_seconds"' +\
        ' FROM songs INNER JOIN genres ON songs.genre=genres.id WHERE'

    if artist:
        query += ' artist LIKE ' + "'" + '%' + str(artist) + '%' + "'" + ' COLLATE NOCASE AND'

    if song:
        query += ' title LIKE ' + "'" + '%' + str(song) + '%' + "'" + ' COLLATE NOCASE AND'
    
    if genre:
        query += ' name LIKE ' + "'" + '%' + str(genre) + '%' + "'" + ' COLLATE NOCASE AND'

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
            int(min_length)
            float(min_length)
        except:
            if len(min_length.split(':')) == 2 or len(min_length.split(':')) == 3:
                min_length = convert_time(min_length)
        query += ' duration>=' + str(min_length) + ' AND'

    if max_length:
        try:
            int(max_length)
            float(max_length)
        except:
            if len(max_length.split(':')) == 2 or len(max_length.split(':')) == 3:
                max_length = convert_time(max_length)
        query += ' duration<=' + str(max_length) + ' AND'

    query = query[:-4] + ';'

    if artist == None and song == None and \
        genre == None and min_length == None and max_length == None:
        results = {'Error': 'Incorrect Input!'}
    else:
        cnx = sqlite3.connect('../data/bvde.db')
        cnx.row_factory = make_dicts
        cur = cnx.cursor()
        results = cur.execute(query).fetchall()

    return jsonify(results)

@app.route('/genres', methods=['GET'])
def all_genres():
    cnx = sqlite3.connect('../data/bvde.db')
    cnx.row_factory = make_dicts
    cur = cnx.cursor()
    genres = cur.execute('SELECT name AS "genre_name", genres.id AS "genre_id",' +\
        ' sum(duration) AS "aggregated_duration_in_seconds",' +\
        ' count(songs.title) AS "genre_count" FROM genres' +\
        ' LEFT JOIN songs on songs.genre = genres.id' +\
        ' GROUP BY genres.name ORDER BY genres.id asc;').fetchall()

    return jsonify(genres)

if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0')