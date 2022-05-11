"""Testing our song management"""
from app.db import db
from app.db.models import Song

def test_retrieve_song(client, add_user, write_test_csv):
    """Test viewing an uploaded song"""
    # login to be able to upload a csv
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    file = open("music.csv", 'rb')
    # upload the csv
    client.post('/songs/upload', data={'file': file})

    # assert that we get the song's information on it's view page
    response = client.get('api/song/1')
    assert b"Song Information" in response.data
    assert b"Title: Move" in response.data
    assert b"Artist: TobyMac" in response.data

    # assert that our spotify api worked
    # if it was able to get the track id with the api, it should have loaded the embedded iframe element
    assert b"iframe" in response.data

def test_delete_song(client, add_user):
    """Test that we can delete a song on the browse page"""
    # login to be upload a song
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a song
    client.post('/song/new', data={'title': 'Armies', 'artist': 'KB', 'year': '2020', 'genre': 'Rap'})
    # delete the song
    response = client.post('/song/1/delete')
    # assert that we get redirected to the browse page
    assert '/songs' in response.headers['Location']
    assert response.status_code == 302

    # check that the song was removed from the db
    assert db.session.query(Song).count() == 0

    response = client.get("/songs")
    # assert that we get the expected flash message
    assert b"Song Deleted" in response.data


def test_add_song(client, add_user):
    """Test that we can add a song using the add song page"""
    # login to be able to upload a csv
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a song
    response = client.post('/song/new', data={'title': 'Armies', 'artist': 'KB', 'year': '2020', 'genre': 'Rap'})

    # check that the song was added to the db
    assert db.session.query(Song).count() == 1
    song = Song.query.filter_by(title='Armies').first()
    assert song.title == "Armies"
    assert song.artist == "KB"
    assert song.year == "2020"
    assert song.genre == "Rap"

    # assert that we get redirected to the browse page
    assert '/songs' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/songs")
    # assert that we get the expected flash message
    assert b"Song added successfully" in response.data


def test_edit_song(client, add_user):
    """Test that we can edit a song using the edit song page"""
    # login to be able to upload a csv
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a song
    client.post('/song/new', data={'title': 'Armies', 'artist': 'KB', 'year': '2020', 'genre': 'Rap'})
    # edit/update the song info
    response = client.post('/song/1/edit', data={'title': 'New Song', 'artist': 'KB', 'year': '2020', 'genre': 'Rap'})

    # assert that we get redirected to the browse page
    assert '/songs' in response.headers['Location']
    assert response.status_code == 302

    response = client.get("/songs")
    # assert that we get the expected flash message
    assert b"Song edited successfully" in response.data

    # check that the song was updated in the db
    song = Song.query.filter_by(title='Armies').first()
    assert song is None
    song = Song.query.filter_by(title='New Song').first()
    assert song.title == "New Song"
