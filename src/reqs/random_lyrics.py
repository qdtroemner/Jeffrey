import requests
from random import randint

BASE_URL = 'https://api.genius.com/'
TOKEN = 'Al7fLMpBdgJgx418xDwsFYI5DlWjKQj7jn2sX3Pg4pYmnQcTlEEgpTxjwUh3kNXl'

def get_song(id):
	url = BASE_URL + f'songs/{id}'
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

def get_lyrics(song):
	lyrics = song["response"]