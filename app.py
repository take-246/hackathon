from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.playlist_all'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class AllPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(128), nullable=False)
    song = db.Column(db.String(128), nullable=False)
    playlist = db.Column(db.String(128), nullable=False)


@app.route('/')
def index():
    playlists_name = db.session.query(AllPlaylist.playlist).group_by(AllPlaylist.playlist).all()
    playlists_name = [p[0] for p in playlists_name]
    return render_template('index.html', playlists_name=playlists_name)

@app.route('/playlist/<name>')
def show_playlist(name):
    playlist_data = db.session.query(AllPlaylist).filter_by(playlist=name)
    return render_template('playlist.html', playlist=playlist_data)

@app.route('/edit')
def edit():
    return render_template('edit.html')


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run()