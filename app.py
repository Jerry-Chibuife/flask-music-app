from _datetime import datetime
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request

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
    if request.method == 'POST':
        artiste = request.form['artiste_name']
        song_name = request.form['title']
        album_name = request.form['album']
        song_genre = request.form['genre']
        song_desc = request.form['desc']
        db.song.insert_one({'artiste_name': artiste, 'song_title': song_name, 'album_name': album_name,
                            'genre': song_genre, 'desc': song_desc, 'date_added': datetime.utcnow().__str__()})
        return render_template('musicForm.html')
    return render_template('musicForm.html')


@app.route('/song/edit/<song_id>', methods=['PATCH', 'GET'])
def edit_song_details(song_id):
    if request.method == 'PATCH':
        song = db.song.find({'_id': ObjectId(song_id)})
        if request.form['artiste_name'] != "":
            artiste = request.form['artiste_name']
        else:
            artiste = song.artiste_name
        if request.form['song_title'] != "":
            song_name = request.form['song_title']
        else:
            song_name = song.song_title
        if request.form['album_name'] != "":
            album_name = request.form['album_name']
        else:
            album_name = song.album_name
        if request.form['genre'] != "":
            song_genre = request.form['genre']
        else:
            song_genre = song.genre
        if request.form['desc'] != "":
            song_desc = request.form['desc']
        else:
            song_desc = song.desc
        db.song.update({'artiste_name': artiste, 'song_title': song_name, 'album_name': album_name,
                        'genre': song_genre, 'desc': song_desc, 'date_added': datetime.utcnow().__str__()})
    return render_template('songList.html', list_of_songs=db.song.find())


@app.route('/song/delete/<song_id>')
def delete_song(song_id):
    db.song.find_one_and_delete({'_id': ObjectId(song_id)})
    return render_template('songList.html', list_of_songs=db.song.find())


@app.route('/songs')
def get_All_Songs():
    list_of_songs = db.song.find()
    return render_template('songList.html', list_of_songs=list_of_songs)


if __name__ == '__main__':
    app.run(debug=True)
