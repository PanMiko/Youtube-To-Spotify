from youtubeClient import YouTubeClient
from spotifyClient import SpotifyClient

from credentials.credentails import SPOTIFY_AUTH_TOKEN
from credentials.credentails import SPOTIFY_USER_ID

import requests

YOUTUBE_CREDS = "./credentials/youtube_creds.json"

def main():
    youtubeClient = YouTubeClient(YOUTUBE_CREDS)
    spotifyClient = SpotifyClient(SPOTIFY_AUTH_TOKEN, SPOTIFY_USER_ID)

    ytPlaylists = youtubeClient.getAllPlaylists()
    print(">>> (YOUTUBE) CHOOSE FROM WHICH PLAYLIST YOU WANT GET SONGS:")

    while True:
        for i, playlist in enumerate(ytPlaylists):
            print(f"{i + 1}. {playlist.title}")
        
        try:
            ytChoice = int(input("\n>>> Your choice: "))
        except ValueError:
            pass

        if ytChoice > 0 and ytChoice <= len(ytPlaylists):
            break
        else:
            print("\n!!! WRONG CHOICE !!!\n")

    chosenYTPlaylist = ytPlaylists[ytChoice - 1]

    spotifyPlaylists = spotifyClient.getPlaylists()
    print(">>> (SPOTIFY) CHOOSE TO WHICH PLAYLIST YOU WANT ADD SONGS:")

    while True:
        for i, playlist in enumerate(spotifyPlaylists):
            print(f"{i + 1}. {playlist.title}")
        
        try:
            spotifyChoice = int(input("\n>>> Your choice: "))
        except ValueError:
            pass

        if spotifyChoice > 0 and spotifyChoice <= len(spotifyPlaylists):
            break
        else:
            print("\n!!! WRONG CHOICE !!!\n")

    chosenSpotifyPlaylist = spotifyPlaylists[spotifyChoice - 1]

    print(f"\n\n\n\n>>> FROM: {chosenYTPlaylist.title}")
    print(f">>> TO: {chosenSpotifyPlaylist.title}\n\n\n\n")
    

    songs, allSongsOnYT = youtubeClient.getVideosFromSpecificPlaylist(chosenYTPlaylist.id)

    # print(">>> Getted songs: ")
    # for song in songs:
    #     print(f"{song.artist} - {song.track}")

    howManyNotFound = 0
    for song in songs:
        trackURI = spotifyClient.searchSong(song.artist, song.track)

        if trackURI != None:
            spotifyClient.addSong(trackURI, chosenSpotifyPlaylist.id)
        
        else:
            print(f">>> SONG NOT FOUND ON SPOTIFY ({song.artist} - {song.track}) <<<")
            howManyNotFound += 1

    print("\n")
    print(f">>> songs in YT playlist:                           {allSongsOnYT}")
    print(f">>> songs SUCCESSFUL DOWNLOADED from YT:            {len(songs)}")
    print(f">>> songs SUCCESSFUL SAVED on SPOTIFY playlist:     {len(songs) - howManyNotFound}")
    print(f">>> songs not founded on Spotify:                   {howManyNotFound}\n")

if __name__ == "__main__":
    main()