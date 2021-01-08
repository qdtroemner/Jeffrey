import requests
import re
from random import randint

GENIUS_URL = 'https://api.genius.com/'
TOKEN = 'Al7fLMpBdgJgx418xDwsFYI5DlWjKQj7jn2sX3Pg4pYmnQcTlEEgpTxjwUh3kNXl'

LYRICS_URL = 'https://api.lyrics.ovh/v1/'

def get_song(id):
	url = GENIUS_URL + f'songs/{id}'
	params = {
		"access_token": TOKEN
	}
	data = requests.get(url, params=params).json()
	if data["meta"]["status"] != 200:
		return False
	return data

def get_random_song():
	song = get_song(randint(1, 6000000))
	if song:
		return song
	else:
		get_random_song()

def get_lyrics(artist, song):
	artist = artist.replace(" ", "%20")
	song = song.replace(" ", "%20")

	url = LYRICS_URL + f'{artist}/{song}'
	if not artist or not song:
		print("Missing artist or song input.")
		return False
	
	request = requests.get(url)
	lyrics = request.json()
	if request.status_code != requests.codes.ok:
		print(f"Status code error. {request.status_code}")
		return False

	lyrics = lyrics["lyrics"].split('\n\n\n\n')
	formatted_lyrics = []
	for index, verse in enumerate(lyrics):
		formatted_lyrics.append(re.sub('\\n\\n|\\r\\n', '\n', verse))

	return formatted_lyrics