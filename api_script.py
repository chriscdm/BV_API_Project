from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
import sqlite3
#import os

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Home</h1>"

@app.route('/all_songs', methods=['GET'])
def api_all():
    cnx = sqlite3.connect('/Users/christophermarker/Documents/BV_API_Project/bvde.db')
    all_songs = cnx.execute('SELECT * FROM songs;').fetchall()

    return jsonify(all_songs)


app.run()
