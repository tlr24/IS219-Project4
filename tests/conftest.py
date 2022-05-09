"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import os
import csv
import pytest
from app import create_app
from app.db import db
from app.db.models import User


@pytest.fixture()
def application():
    """This makes the app"""
    os.environ['FLASK_ENV'] = 'testing'
    application = create_app()
    application.config.update({
        "TESTING": True,
        "WTF_CSRF_METHODS": [],
        "WTF_CSRF_ENABLED": False
    })
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()

@pytest.fixture
def add_user(client):
    """Add a user for testing"""
    client.post("register", data={"email": "a@a.com", "password": "123La!", "confirm": "123La!"})

@pytest.fixture()
def add_user_to_db():
    user = User('a@gmail.com', '123La!', 0)
    db.session.add(user)
    db.session.commit()

@pytest.fixture()
def write_test_csv():
    # write a dummy csv file for testing
    header = ['Name', 'Artist', 'Year', 'Genre']
    data = [
        ['Move (Keep Walkin’)', "TobyMac", '2015', 'Christian'],
        ['Edge Of My Seat', "TobyMac", '2018', 'Christian'],
    ]

    with open('music.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)