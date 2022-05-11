[![Production Workflow](https://img.shields.io/github/workflow/status/tlr24/IS219-project4/Production%20Workflow%201?label=Production%20Workflow%201&logo=github)](https://github.com/tlr24/IS219-project4/actions/workflows/prod.yml)

* [Production Deployment](https://tlr24-is219-prod4.herokuapp.com/)


[![Development Workflow](https://img.shields.io/github/workflow/status/tlr24/IS219-project4/Development%20Workflow%203.8?label=Development%20Workflow%203.8&logo=github)](https://github.com/tlr24/IS219-project4/actions/workflows/dev.yml)

* [Developmental Deployment](https://tlr24-is219-dev4.herokuapp.com/)

### Purpose
The purpose of this project is for users to be able to register/login/logout and also to be able to upload a csv of their favorite songs and see the link to the album on Spotify as well as to be able to play the song and the other top tracks from the artist through Spotify directly on the song's view page.

### Features
Users can upload song csvs including the song's title, artist, year, and genre that will be processed into the SQLite database and will be displayed in the user's dashboard. 

On the dashboard there will be a view button on each song which will take the user to the song's view page. Once the view button is clicked, the app uses JavaScript to call the Spotify API to search for the song and retrieve its song's album name, album link on Spotify, Spotify track id, and Spotify artist id. It uses the song title and artist from the csv/db in the query of the Spotify API call. It then inserts the track id into an embedded Spotify music player for the song and it embeds the artist id into an embedded Spotify music player for the top tracks by the artist.

This way, users can automatically get a link to a song's album and be able to play the song and other top tracks from the artist all from the view page.

There are also user and song management pages for use by admins.

### Setup Notes
For the Spotify API calls to work locally, a .env file has to be created at the root of the project. The .env file must include: "SPOTIFY_API_KEY=" followed by the Spotify API key that the project will use.

In Heroku, the Spotify API key must be included as a Config Var with the key of "SPOTIFY_API_KEY" with the api key included as the value. The Config Var can be set on the Heroku app through Settings --> Reveal Config Vars.
