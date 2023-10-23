from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://www.billboard.com/charts/hot-100",
        client_id="ADD-YOURS-HERE",
        client_secret="ADD-YOURS-HERE",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Enter a date(YYYY-MM-DD)" )


response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
top_100 = response.text


soup = BeautifulSoup(top_100, "html.parser")

data = soup.findAll(name="span", class_="chart-element__information__song text--truncate color--primary")

titles = [name.get_text() for name in data]



song_uris = []
year = date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)
