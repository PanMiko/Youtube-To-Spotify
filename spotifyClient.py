import requests
import urllib.parse


class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title

class SpotifyClient(object):
    def __init__(self, apiToken, userId):
        self.apiToken = apiToken
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
            # print(responseJSON['items'][item]['name'])

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
                return None
        except KeyError:
            print(">>> !!! KEYERROR")
            return None

        return responseJSON['tracks']['items'][0]['uri']


    def addSong(self, trackURI, playlistId):
        url = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?uris={trackURI}"

        response = requests.post(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.apiToken}"  
            }
        )

        responseJSON = response.json()

        return response.ok


    
