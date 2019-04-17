import spotipy              
import spotipy.util         as util
from spotipy.oauth2         import SpotifyClientCredentials
from myconfig               import *




#{track_name, artist, date_added, duration_ms, popularity, track_id}
def GetTracks(tracks, trackList):
    for count, item in enumerate(tracks['items']):
        track_id = item['track']['id']
        trackList.append(track_id)

#returns list of dicts from GetTracks
def GetPlaylist(username, playlist_id):
    playlist = sp.user_playlist(username,playlist_id)
    tracks = playlist['tracks']#['items']
    trackList = []
    GetTracks(tracks, trackList)
    while tracks['next']:
        tracks = sp.next(tracks)
        GetTracks(tracks, trackList)
    return trackList






scope = 'playlist-modify-private'
token = util.prompt_for_user_token(PLAYLIST_OWNER, scope)

if token:
    ccm = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=ccm, auth=token)
    sp.trace=False
    tracks = GetPlaylist(PLAYLIST_OWNER, DISCOVER_WEEKLY_ID)
    sp.user_playlist_add_tracks(PLAYLIST_OWNER, DISC_COPY, tracks)
    print "Done"
    
else:
    print "Error"



#user_playlist_create(user,name,public,description)
#user_playlist_add_tracks(user, playlist_id, tracks, position=None)
#https://open.spotify.com/user/spotify/playlist/37i9dQZEVXcQnLWPyT6fWT?si=_5v_ukMkTwSYQhl-V7ePwA
