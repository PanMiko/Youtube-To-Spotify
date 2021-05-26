import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
import re

from helpers.song import Song
from helpers.playlist import Playlist

BLACK_LIST = ['offical ', 'orginal ', 'video', 'audio', 'ft.', 'feat.', 'lyric', 'extended', 'ft', 'feat', ' x ', ' & ', ' + ', ' vs ', ' / ', ',', ' and ', ' with']
FEAT_LIST = ['ft.', 'feat.', 'feat', 'ft']
WHITE_LIST = ['remix', 'edit']

# YOUTUBECLIENT CLASS---------------------------
class YouTubeClient(object):
    # constructor
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = credentials_location

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        
        credentials = flow.run_local_server()
        
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

        self.youtube = youtube

    # Getting all playlists from YT channel |  returning playlists' array
    def getAllPlaylists(self):
        request = self.youtube.playlists().list(
            part="snippet, contentDetails",
            maxResults = 25,
            mine = True
        )
        response = request.execute()

        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists

    # Getting all music videos from specific playlist | returning songs' array 
    def getVideosFromSpecificPlaylist(self, searchedPlaylistId):
        request = self.youtube.playlistItems().list(
            playlistId = searchedPlaylistId,
            part = "id, snippet",
            maxResults = 50
        )
        response = request.execute()

        songs = []

        for item in response['items']:
            videoId = item['snippet']['resourceId']['videoId']

            artist, track = self.getArtistAndTitle(videoId)

            if artist != None and track != None:
                songs.append(Song(artist, track))

        temp = len(response['items'])
        totalResults = response['pageInfo']['totalResults']
        
        while temp < totalResults:
            nextPageToken = response['nextPageToken']
            request = self.youtube.playlistItems().list(
                playlistId = searchedPlaylistId,
                part = "id, snippet",
                maxResults = 50,
                pageToken = nextPageToken
            )
            response = request.execute()

            temp += len(response['items'])

            for item in response['items']:
                videoId = item['snippet']['resourceId']['videoId']

                artist, track = self.getArtistAndTitle(videoId)

                if artist != None and track != None:
                    songs.append(Song(artist, track))
        
        return songs, totalResults

    # Getting and returning artist and title of song
    def getArtistAndTitle(self, videoId):
        yt_url = f"https://www.youtube.com/watch?v={videoId}"

        try:
            video = youtube_dl.YoutubeDL().extract_info(yt_url, download = False)
        except youtube_dl.utils.DownloadError:
            print(">>> Video unavailable ERROR")
            return None, None

        artist = ""
        track = ""

        try:
            artist = video['artist']
            track = video['track']
        except KeyError:
            print(">>> artist & title ERROR")
            artist, track = self.unknownArtistAndTitle(video['title'])
            print(f">>> : {artist} - {track}")


        if artist != None and track != None:
            artist = self.shellingOut(artist)
            track = self.shellingOut(track)

        return artist, track
# -------------------------------------

    def unknownArtistAndTitle(self, unknown):
        unknown = unknown.lower()

        results = [m.start() for m in re.finditer(' - ', unknown)]
        if results == []:
            results = [m.start() for m in re.finditer(' – ', unknown)]

        if results == []:
            return None, None

        result = results[0]

        if len(results) > 1 and (ord(unknown[0]) < 97 or ord(unknown[0]) > 122):
            unknown = unknown[result + 3:]
            result = results[1] - (result + 3)

        artist = self.shellingOut(unknown[:result])
        track = self.shellingOut(unknown[result + 3:])

        return artist, track
    
    def shellingOut(self, text):
        text = text.lower()
        
        for word in BLACK_LIST:
            text = text.replace(word, ' ')

        if '[' in text:
            try:
                lastIndex = text.index(']') + 1
            except ValueError: 
                lastIndex = 0
            text = text[:text.index('[')] + text[lastIndex:]

        if '|' in text:
            text = text[:text.index('|')]

        x = [m.start() for m in re.finditer('\(', text)] + [m.start() for m in re.finditer('\)', text)]
        x.sort()

        temp = text

        i = 0
        while i < len(x):
            s = text[x[i] : x[i + 1] + 1]
            if not any(word in s for word in WHITE_LIST):
                temp = temp.replace(s, ' ')

            i += 2
        
        for x in FEAT_LIST:
            temp = temp.replace(x, ' ')

        return temp