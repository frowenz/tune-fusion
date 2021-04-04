# Libraries
from spotipy.client import Spotify
import sys
import pandas as pd
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# Credentials
client_id = '77babaa06e88474c839e202c43b4bccf'
secret_id = '90148a0d040a40998e750a819f43dcc7'
redirect_uri = 'http://localhost:8000'

# NEED TO TURN THIS INTO USER INPUT
username = 'biu_indigo' 
input_playlist_name = 'Joint Playlist'
fused_list = ['0jfeHptByz7p6pa2LhP8lx', '0jfeHptByz7p6pa2LhP8lx'] # LIST OF IDS IN ORDER

#Authorize
scope = "playlist-modify-private"
token = util.prompt_for_user_token(username, scope, client_id, secret_id, redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

#Builds playlist
def new_playlist(sp, username, playlist_name, playlist_description):
    playlists = sp.user_playlist_create(username, playlist_name, public = False, description = playlist_description)

new_playlist(sp, username, input_playlist_name, 'Made with tune-fusion: https://uncommon.carolynmh.repl.co/testpage')

#Fetch user's playlist library
def get_playlists(sp, username):
        
    id = []
    name = []
    num_tracks = []
    
    # Make the API request
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        id.append(playlist['id'])
        name.append(playlist['name'])
        num_tracks.append(playlist['tracks']['total'])

    # Create the final df   
    df_playlists = pd.DataFrame({"id":id, "name": name, "#tracks": num_tracks})
    return df_playlists

get_playlists(sp,username).head(3)

#Get our playlist id
new_id = get_playlists(sp,username).id
print (new_id)

#Add Tracks 
sp.user_playlist_add_tracks(username, new_id, fused_list, position=None)
