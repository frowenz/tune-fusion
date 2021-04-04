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

# Builds playlist and returns new Playlist object
def new_playlist(sp, username, playlist_name, playlist_description):
    playlist = sp.user_playlist_create(username, playlist_name, public = False, description = playlist_description)
    return playlist

def create_joint_playlist(username, name2, input_playlist_name):
    # Authorize
    token = util.prompt_for_user_token(username, scope, client_id, secret_id, redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    
    # use last.fm data and spotify features to gather a list of song ids
    fused_list = script.get_shared_playlist(username, name2)
    # print(fused_list)

    # Create the new playlist and get the playlist id
    pl = new_playlist(sp, username, input_playlist_name, 'Made with tune-fusion: https://uncommon.carolynmh.repl.co/testpage')
    new_id = pl['id']
    pl_name = pl['name']
    # print(f"new id = {new_id} for playlist \"{pl_name}\"")

    #Add Tracks 
    # print("Adding tracks to new playlist...")
    sp.user_playlist_add_tracks(username, new_id, tracks=fused_list, position=None)

# for testing purposes
if __name__ == "__main__":
    name1 = input("Your last.fm username: ")
    name2 = input("Your friend's last.fm username: ")
    playlist_name = input("Playlist name: ")
    create_joint_playlist(name1, name2, playlist_name)
