import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd

SPOTIPY_CLIENT_ID = "21732af26e344c0ca09a681b2cde2253"
SPOTIPY_CLIENT_SECRET  = "3cd6b42776f8489cb18bea190d7d98f5"
# os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
# os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def get_song_info(artist, song):
    # assume that the first result is the correct song
    results = spotify.search(q=f'{artist} {song}', limit=1, type="track")
    item = results['tracks']['items'][0]
    artist_uri = item['artists'][0]['uri'] # just go with the first artist if there are multiple
    song_uri = item['uri']
    duration_ms = item['duration_ms']
    explicit = item['explicit']
    album = item['album']['name']
    popularity = item['popularity']
    return artist, artist_uri, song, song_uri, duration_ms, explicit, album, popularity

def add_features(user1_songs, user2_songs):
    user1_list = []
    for song in user1_songs['song_uri']:
        row = pd.DataFrame(spotify.audio_features(tracks=[song]))
        user1_list.append(row)
    user1_df = pd.concat(user1_list)

    user2_list = []
    for song in user2_songs['song_uri']:
        row = pd.DataFrame(spotify.audio_features(tracks=[song]))
        user2_list.append(row)
    user2_df = pd.concat(user2_list)

    dfs = [user1_df, user2_df]
    dfs = pd.concat(dfs)
    # drop unnecessary features
    dfs.drop(['type','track_href','analysis_url','time_signature','duration_ms','uri','instrumentalness','liveness','loudness','key','mode'],1,inplace=True)
    dfs.set_index('id',inplace=True)
    return dfs

def get_recs(list_of_recs, adj_list_of_recs):
    #Getting 1 recommended song from each cluster with less than 4 songs, 2 recommended songs from each cluster with 4-5 songs
    list_of_recommendations = [0]*len(list_of_recs)
    k = 0
    list_of_recommendations = [0]*len(list_of_recs)
    while k < len(list_of_recs):
        if len(adj_list_of_recs[k]) < 4:
            list_of_recommendations[k] = spotify.recommendations(seed_tracks=adj_list_of_recs[k],limit=1)
        else:
            list_of_recommendations[k] = spotify.recommendations(seed_tracks=adj_list_of_recs[k],limit=2)
        k += 1
    
    return list_of_recommendations