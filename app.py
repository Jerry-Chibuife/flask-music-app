from _datetime import datetime

import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
from cloudinary.utils import cloudinary_url
import os
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request, redirect
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/za-music_db"
mongodb_client = PyMongo(app)
db = mongodb_client.db


# class Song(db.Document):
#     artisteName = db.StringField


@app.route('/')
def hello_world():  # put application's code here
    return render_template('homepage.html')


@app.route('/song/add', methods=['POST', 'GET'])
def upload_song():

    cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'),
                      api_secret=os.getenv('API_SECRET'))
    upload_result = None
    if request.method == 'POST':
        artiste = request.form['artiste_name']
        song_name = request.form['title']
        album_name = request.form['album']
        song_genre = request.form['genre']
        song_desc = request.form['desc']
        file_to_upload = request.files['audioFile']
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload, resource_type="audio")
            app.logger.info(upload_result)
            app.logger.info(type(upload_result))
        db.song.insert_one({'artiste_name': artiste, 'song_title': song_name, 'album_name': album_name,
                            'genre': song_genre, 'desc': song_desc, 'date_added': datetime.utcnow().__str__()})
        return render_template('musicForm.html')
    return render_template('musicForm.html')


@app.route('/song/edit/<song_id>', methods=['POST', 'GET'])
def edit_song_details(song_id):
    song = db.song.find_one({'_id': ObjectId(song_id)})
    if request.method == 'POST':
        artiste = request.form['artiste_name']
        song_name = request.form['title']
        album_name = request.form['album']
        song_genre = request.form['genre']
        song_desc = request.form['desc']

        print(artiste, song_name, album_name, song_genre, song_desc)
        db.song.update_one({'_id': ObjectId(song_id)},
                                    {'$set': {'artiste_name': artiste, 'song_title': song_name,
                                              'album_name': album_name,
                                              'genre': song_genre, 'desc': song_desc}})
        return redirect(url_for('get_All_Songs'))

    return render_template('update_song_details.html', song=song)


@app.route('/song/delete/<song_id>')
def delete_song(song_id):
    db.song.find_one_and_delete({'_id': ObjectId(song_id)})
    return redirect(url_for('get_All_Songs'))


@app.route('/songs')
def get_All_Songs():
    list_of_songs = db.song.find()
    return render_template('songList.html', list_of_songs=list_of_songs)


if __name__ == '__main__':
    app.run(debug=True)
