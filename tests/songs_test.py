"""Tests the songs functionality"""
import os
from app.db.models import db, Song, User


def test_adding_songs(application, add_user_to_db):
    """Test adding songs"""
    with application.app_context():
        user = User.query.filter_by(email="a@gmail.com").first()
        # prepare songs to insert
        user.songs = [Song("title1", "artist1", "2020", "Rap"), Song("title2", "artist2", "2022", "Pop")]
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='title1').first()
        assert song1.title == "title1"

def test_updating_songs(application, add_user_to_db):
    """Test updating song"""
    with application.app_context():
        user = User.query.filter_by(email="a@gmail.com").first()
        # prepare songs to insert
        user.songs = [Song("title1", "artist1", "2020", "Rap")]
        db.session.commit()
        # changing the title of the song
        song = Song.query.filter_by(title='title1').first()
        song.title = "New Song"
        db.session.commit()
        updated_song = Song.query.filter_by(title='New Song').first()
        assert updated_song.title == "New Song"

def test_deleting_song(application, add_user_to_db):
    """Test deleting the song"""
    user = User.query.filter_by(email="a@gmail.com").first()
    # prepare songs to insert
    user.songs = [Song("title1", "artist1", "2020", "Rap")]
    db.session.commit()
    song = Song.query.filter_by(title='title1').first()
    # delete the song
    db.session.delete(song)
    #assert db.session.query(Song).count() == 0

def test_upload_csv(client, add_user, write_test_csv):
    """Test uploading and processing a csv file"""
    # login to be able to upload the csv
    response = client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    file = open("music.csv", 'rb')
    # upload the csv
    response = client.post('/songs/upload', data={'file': file})
    assert "/songs" in response.headers["Location"]
    assert response.status_code == 302

    root = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(root, '../uploads/music.csv')
    # check that the file was uploaded
    assert os.path.exists(csv_file) == True

    # test that the csv file was processed and the songs were inserted into the database
    user = User.query.filter_by(email="a@a.com").first()
    assert len(user.songs) == 2
    assert db.session.query(Song).count() == 2
    assert Song.query.filter_by(title="Move (Keep Walkin’)").first() is not None
    assert Song.query.filter_by(title="Edge Of My Seat").first() is not None

def test_create_upload_folder():
    """Test if uploads folder is being created"""
    # Uploads folder should be created at start
    root = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.join(root, '../uploads')
    # check if the directory exists
    assert os.path.exists(uploads_dir) == True