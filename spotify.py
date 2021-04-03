from bottle import request
import spotipy
from spotipy import oauth2
import os

SPOTIPY_CLIENT_ID = "21732af26e344c0ca09a681b2cde2253"
SPOTIPY_CLIENT_SECRET  = "2ebe7cced83d43698a5dcc994d274d57"

PORT_NUMBER = 8080
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )


access_token = ""

token_info = sp_oauth.get_cached_token()

if token_info:
    print("Found cached token!")
    access_token = token_info['access_token']
else:
    url = request.url
    code = sp_oauth.parse_response_code(url)
    if code != url:
        print("Found Spotify auth code in Request URL! Trying to get valid access token...")
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']


# def get_song(artist, song_title):
#     # song_title = song_title.replace(' ', '%20')
#     # artist = artist.replace(' ', '%20')
#     results = spotify.search(q=f'track:{song_title}%20artist:{artist}', limit=3, type="track")
#     print(results)