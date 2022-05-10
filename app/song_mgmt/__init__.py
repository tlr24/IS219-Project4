from flask import Blueprint, render_template, jsonify, abort, current_app
from flask_login import login_required
from jinja2 import TemplateNotFound
from app.db.models import Song


song_mgmt = Blueprint('song_mgmt', __name__,
                        template_folder='templates')

@song_mgmt.route('/api/song/<int:song_id>')
@login_required
def retrieve_song(song_id):
    spotify_api_key = current_app.config.get('SPOTIFY_API_KEY')
    song = Song.query.get(song_id)
    song_name = song.title.replace(" ", "%20")
    song_artist = song.artist.replace(" ", "%20")
    return render_template('song_view.html', song=song, song_id=song_id, song_name=song_name, song_artist=song_artist, spotify_api_key=spotify_api_key)
