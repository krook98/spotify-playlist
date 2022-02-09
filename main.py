from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# If this doesn't work, try passing cid and secret directly to variables instead of using export/set
cid = os.environ.get('SPOTIPY_CLIENT_ID')
secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=cid,
        client_secret=secret,
        redirect_uri="http://example.com",
        cache_path='.cache',
        scope='playlist-modify-private'
    )
)

user_id = spotify.current_user()['id']

choose_date = input('Type the date in format YYYY-MM-DD to create a playlist for a specific day: ')
response = requests.get(url=f'https://www.billboard.com/charts/hot-100/{choose_date}/')
page = response.text

soup = BeautifulSoup(page, 'html.parser')
songs = soup.select(selector="li h3",id="title-of-a-story")
list = []

for song in songs:
    list.append(song.getText().split("\n")[1])
    song_list = list[0:100]

results = []
year = choose_date.split('-')[0]
for song in song_list:
    song_on_spotify = spotify.search(q='track: ' + song + ' year: ' + year, type='track')
    try:
        uri = song_on_spotify['tracks']['items'][0]['uri']
        results.append(uri)
    except IndexError:
        print(f"{song} doesn't exist on Spotify")

new_playlist = spotify.user_playlist_create(user=user_id, name=f"Top 100 z pierwszego dnia zwiazku :)", public=False, collaborative=False)
spotify.playlist_add_items(playlist_id=new_playlist['id'], items=results)


