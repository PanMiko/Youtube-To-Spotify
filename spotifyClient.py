import requests

from credentials.credentails import REFRESH_TOKEN, BASE_64
from helpers.song import Song
from helpers.playlist import Playlist

class SpotifyClient(object):
    def __init__(self, userId):
        self.apiToken = self.refreshToken()
        self.userId = userId

    def getPlaylists(self):
        url = f"https://api.spotify.com/v1/users/{self.userId}/playlists"

        response = requests.get(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.apiToken}"  
            }
        )

        responseJSON = response.json()

        playlists = []

        for item in range(len(responseJSON['items'])):
            playlists.append(Playlist(responseJSON['items'][item]['id'], responseJSON['items'][item]['name']))

        return playlists


    def searchSong(self, artist, track):
        url = f"https://api.spotify.com/v1/search?q={artist} {track}&type=track"

        response = requests.get(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.apiToken}"  
            }
        )

        responseJSON = response.json()
        try:
            if not responseJSON['tracks']['items']:
                return None, None
        except KeyError:
            print(">>> !!! KEYERROR")
            return None, None

        artistAndTitle = ''
        for artist in responseJSON['tracks']['items'][0]['artists']:
            artistAndTitle += str(artist['name']) + ', '
        artistAndTitle = artistAndTitle[:-2]

        title = responseJSON['tracks']['items'][0]['name']
        
        url_img = responseJSON['tracks']['items'][0]['album']['images'][1]['url']
        
        return responseJSON['tracks']['items'][0]['uri'], Song(artistAndTitle, title, url_img)


    def addSong(self, trackURI, playlistId):
        url = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?uris={trackURI}"

        response = requests.post(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.apiToken}"  
            }
        )

        return response.ok

    def refreshToken(self):
        url = "https://accounts.spotify.com/api/token"

        response = requests.post(url,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": REFRESH_TOKEN},
                                 headers={"Authorization": "Basic " + BASE_64})

        response_json = response.json()
        print(response_json)

        return response_json["access_token"]


    
