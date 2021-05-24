# Get all playlists from Youtube
def getPlaylists(youtubeClient, spotifyClient):
        ytPlaylists = youtubeClient.getAllPlaylists()

        print(">>> YOUTUBE:")
        for i, playlist in enumerate(ytPlaylists):
                print(f"{i + 1}. {playlist.title}")

        spotifyPlaylists = spotifyClient.getPlaylists()
        print(">>> SPOTIFY:")
        for i, playlist in enumerate(spotifyPlaylists):
                print(f"{i + 1}. {playlist.title}")

        return ytPlaylists, spotifyPlaylists

# Starting converting songs from YT to Spotify
def startConvert(chosenYTPlaylist, chosenSpotifyPlaylist, youtubeClient, spotifyClient):
        print(f"\n\n\n\n>>> FROM: {chosenYTPlaylist.title}")
        print(f">>> TO: {chosenSpotifyPlaylist.title}\n\n\n\n")

        songs, allSongsOnYT = youtubeClient.getVideosFromSpecificPlaylist(chosenYTPlaylist.id)
        successSavedOnSpotify = []

        howManyNotFound = 0
        for song in songs:
                trackURI, artistsAndTitle = spotifyClient.searchSong(song.artist, song.track)

                if trackURI != None:
                        spotifyClient.addSong(trackURI, chosenSpotifyPlaylist.id)
                        successSavedOnSpotify.append(artistsAndTitle)
                        
                else:
                        print(f">>> SONG NOT FOUND ON SPOTIFY ({song.artist} - {song.track}) <<<")
                        howManyNotFound += 1

        statistics = []
        print("\n")
        print(f">>> Songs in YT playlist:                           {allSongsOnYT}")
        statistics.append(f"Songs in YT playlist: {allSongsOnYT}")
        print(f">>> Songs SUCCESSFUL DOWNLOADED from YT:            {len(songs)}")
        statistics.append(f"Songs SUCCESSFUL DOWNLOADED from YT: {len(songs)}")
        print(f">>> Songs SUCCESSFUL SAVED on SPOTIFY playlist:     {len(songs) - howManyNotFound}")
        statistics.append(f"Songs SUCCESSFUL SAVED on SPOTIFY playlist: {len(songs) - howManyNotFound}")
        print(f">>> Songs not founded on Spotify:                   {howManyNotFound}\n")
        statistics.append(f"Songs not founded on Spotify: {howManyNotFound}\n")

        # [gui.convertedSongsWidget.addItem(f"{item.artist} - {item.track}") for item in successSavedOnSpotify]
        # gui.converted = successSavedOnSpotify
        # gui.statistics = statistics
        # gui.moreStatisticsBtn.setEnabled(True)

        return successSavedOnSpotify, statistics