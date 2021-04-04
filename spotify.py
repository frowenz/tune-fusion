import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd

SPOTIPY_CLIENT_ID = "21732af26e344c0ca09a681b2cde2253"
SPOTIPY_CLIENT_SECRET  = "3cd6b42776f8489cb18bea190d7d98f5"

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def get_song_id(artist, song):
    # assume that the first result is the correct song
    # if song title has parentheticals, remove them
    while '(' in song:
        i1 = song.find('(')
        i2 = song.find(')')
        song = song[:i1] + song[i2+1:]
    results = spotify.search(q=f'{artist} {song}', limit=1, type="track")
    if len(results['tracks']['items']) == 0:
        return ""
    item = results['tracks']['items'][0]
    song_uri = item['uri'][14:]
    return song_uri


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
        row = spotify.audio_features(tracks=[song])
        # row[0]['weight'] = user1_songs.loc[song].weight
        row = pd.DataFrame(row)
        user1_list.append(row)
    user1_df = pd.concat(user1_list)
    user1_df['weight'] = user1_songs['weight']

    user2_list = []
    for song in user2_songs['song_uri']:
        row = spotify.audio_features(tracks=[song])
        # row[0]['weight'] = song.weight
        row = pd.DataFrame(row)
        user2_list.append(row)
    user2_df = pd.concat(user2_list)
    user2_df['weight'] = user2_songs['weight']

    dfs = [user1_df, user2_df]
    dfs = pd.concat(dfs)
    # drop unnecessary features
    dfs.drop(['type','track_href','analysis_url','time_signature','duration_ms','uri','instrumentalness','liveness','loudness','key','mode'],1,inplace=True)
    dfs.set_index('id',inplace=True)
    return dfs

def get_recs(recs, N=30):
    result = []
    total_weight = sum([w * len(r) for r, w in recs])
    total_recs = 0
    for rec, weight in recs:
        num_recs = int(round(N * weight * len(rec) / total_weight))
        if num_recs <= 0:
            continue
        result.append(spotify.recommendations(seed_tracks=rec,limit=num_recs))
        total_recs += num_recs
    return result, total_recs

def info_from_id(song_id):
    track = spotify.track(song_id)
    return track