# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# Imports
import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth


# Access user content
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
scope = "user-library-read user-read-recently-played user-top-read"
auth_manager = SpotifyOAuth(
    client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist_id = "spotify:playlist:51u8YScD1Ror4je8uh0DHn"
results = sp.playlist(playlist_id)

ids = []

for item in results['tracks']['items']:
    track = item['track']['id']
    ids.append(track)


song_meta = {'id': [], 'album': [], 'name': [],
             'artist': [], 'explicit': [], 'popularity': []}

for song_id in ids:
    meta = sp.track(song_id)
    song_meta['id'].append(song_id)
    album = meta['album']['name']
    song_meta['album'] += [album]
    song = meta['name']
    song_meta['name'] += [song]
    s = ', '
    artist = s.join([singer_name['name'] for singer_name in meta['artists']])
    song_meta['artist'] += [artist]

    explicit = meta['explicit']
    song_meta['explicit'].append(explicit)
    popularity = meta['popularity']
    song_meta['popularity'].append(popularity)

song_meta_df = pd.DataFrame.from_dict(song_meta)
features = sp.audio_features(song_meta['id'])
features_df = pd.DataFrame.from_dict(features)
df = song_meta_df.merge(features_df)
df.to_csv("songs.csv")
