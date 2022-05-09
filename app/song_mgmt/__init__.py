from flask import Blueprint, render_template
from flask_login import login_required
from app.db.models import Song


song_mgmt = Blueprint('song_mgmt', __name__,
                        template_folder='templates')

@song_mgmt.route('/song/<int:song_id>')
@login_required
def retrieve_song(song_id):
    song = Song.query.get(song_id)
    return render_template('song_view.html', song=song)
