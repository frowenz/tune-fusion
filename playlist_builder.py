# Libraries
from spotipy.client import Spotify
import sys
import pandas as pd
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import script

# Credentials
client_id = '77babaa06e88474c839e202c43b4bccf'
secret_id = '90148a0d040a40998e750a819f43dcc7'
redirect_uri = 'http://localhost:8000'
scope = "playlist-modify-private"

def default_playlist_name(name1, name2):
    return f"{name1} and {name2}'s Joint Playlist"

# Builds playlist and returns new Playlist object
def new_playlist(sp, username, playlist_name, playlist_description):
    playlist = sp.user_playlist_create(username, playlist_name, public = False, description = playlist_description)
    return playlist

# this is the magical function right here
def create_joint_playlist(username, name2, input_playlist_name):
    input_playlist_name = input_playlist_name.strip()
    if input_playlist_name == "":
        input_playlist_name = default_playlist_name(username, name2)

    # use last.fm data and spotify features to gather a list of song ids
    fused_list, err = script.get_shared_playlist(username, name2)
    # check for error, returns an error message if users are not found
    if err:
        return fused_list, True

    # Authorize
    token = util.prompt_for_user_token(username, scope, client_id, secret_id, redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    
    # Create the new playlist and get the playlist id
    pl = new_playlist(sp, username, input_playlist_name, 'Made with tune-fusion: https://uncommon.carolynmh.repl.co/testpage')
    new_id = pl['id']

    # Add Tracks 
    sp.user_playlist_add_tracks(username, new_id, tracks=fused_list, position=None)
    return "Success!", False

# for testing purposes
if __name__ == "__main__":
    name1 = input("Your last.fm username: ")
    name2 = input("Your friend's last.fm username: ")
    playlist_name = input("Playlist name: ")
    msg, err = create_joint_playlist(name1, name2, playlist_name)
    if err:
        print(msg)
