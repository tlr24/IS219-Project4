import logging
import os
import csv
from flask_login import login_required, current_user
from flask import current_app, abort, render_template, url_for, Blueprint
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect
from app.db import db
from app.db.models import Song
from app.songs.forms import csv_upload
from app import config

song = Blueprint('songs', __name__, template_folder='templates')

@song.before_app_first_request
def create_upload_folder():
    root = config.Config.BASE_DIR
    uploadfolder = os.path.join(root,'..',config.Config.UPLOAD_FOLDER)
    # make a directory if it doesn't exist
    if not os.path.exists(uploadfolder):
        os.mkdir(uploadfolder)

@song.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def song_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("csv")
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        log.info("User " + str(current_user.get_id()) + " uploaded file: " + filename)
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                song = Song.query.filter_by(title=row['Name']).first()
                if song is None:
                    current_user.songs.append(Song(row['Name'], row['Artist'], row['Year'], row['Genre']))
                    db.session.commit()
                else:
                    current_user.songs.append(song)
                    db.session.commit()

        return redirect(url_for('songs.browse_songs'), 302)
    try:
        return render_template('upload_songs.html', form=form)
    except TemplateNotFound:
        abort(404)

@song.route('/songs', methods=['GET'], defaults={"page": 1})
@song.route('/songs/<int:page>', methods=['GET'])
@login_required
def browse_songs(page):
    page = page
    per_page = 1000
    pagination = Song.query.paginate(page, per_page, error_out=False)
    retrieve_url = ('song_mgmt.retrieve_song', [('song_id', ':id')])
    delete_url = ('song_mgmt.delete_song', [('song_id', ':id')])
    data = pagination.items
    try:
        return render_template('browse_songs.html',data=data,pagination=pagination,retrieve_url=retrieve_url,delete_url=delete_url,Song=Song)
    except TemplateNotFound:
        abort(404)