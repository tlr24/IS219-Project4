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

def test_delete_transaction(client, add_user):
    """Test that we can delete a song on the browse page"""
    # login to be upload a song
    client.post("/login", data={'email': 'a@a.com', 'password': '123La!'})

    # add a song
    file = open("music.csv", 'rb')
    client.post('/songs/upload', data={'file': file})
    # delete the one of the two songs in the test csv
    response = client.post('/song/1/delete')
    # assert that we get redirected to the browse page
    assert '/songs' in response.headers['Location']
    assert response.status_code == 302

    # check that the first out of the two songs in the test csv was removed from the db
    assert db.session.query(Song).count() == 1

    response = client.get("/songs")
    # assert that we get the expected flash message
    assert b"Song Deleted" in response.data