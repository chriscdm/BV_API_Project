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

app.run()
