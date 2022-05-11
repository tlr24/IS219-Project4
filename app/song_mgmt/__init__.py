from flask import Blueprint, render_template, flash, url_for, redirect, current_app
from flask_login import login_required, current_user
from app.db import db
from app.db.models import Song, song_user
from app.song_mgmt.forms import add_song_form, song_edit_form


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


@song_mgmt.route('/song/<int:song_id>/delete', methods=['POST'])
@login_required
def delete_song(song_id):
    db.session.query(song_user).filter_by(user_id=current_user.id, song_id=song_id).delete()
    song = Song.query.get(song_id)
    db.session.delete(song)
    db.session.commit()
    flash('Song Deleted', 'success')
    return redirect(url_for('songs.browse_songs'), 302)

@song_mgmt.route('/song/new', methods=['POST', 'GET'])
@login_required
def add_song():
    form = add_song_form()
    if form.validate_on_submit():
        current_user.songs.append(Song(title=form.title.data, artist=form.artist.data, year=form.year.data, genre=form.genre.data))#user_id=current_user.id))
        db.session.commit()
        flash('Song added successfully', 'success')
        return redirect(url_for('songs.browse_songs'), 302)
    return render_template('song_add.html', form=form)

@song_mgmt.route('/song/<int:song_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_song(song_id):
    song = Song.query.get(song_id)
    form = song_edit_form(obj=song)
    if form.validate_on_submit():
        song.title = form.title.data
        song.artist = form.artist.data
        song.year = form.year.data
        song.genre = form.genre.data
        db.session.add(song)
        db.session.commit()
        flash('Song edited successfully', 'success')
        current_app.logger.info("edited a song")
        return redirect(url_for('songs.browse_songs'))
    return render_template('song_edit.html', form=form)