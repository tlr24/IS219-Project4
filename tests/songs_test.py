"""Tests the songs functionality"""
import pytest
from app.db.models import db, Song, User


@pytest.fixture()
def add_user_to_db():
    user = User('a@gmail.com', '12345678', 0)
    db.session.add(user)
    db.session.commit()

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