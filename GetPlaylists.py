from apiclient.discovery import build
from WriteLog import WriteLog

def GetPlaylists(cId):
    
    service = build('youtube', 'v3', developerKey = 'AIzaSyCuD-M96R2yX4d4o3UVFiBXwAdomxiog-w')

    nextToken = ''

    playlists = []

    while True:
        response = service.playlists().list(part='snippet',channelId=cId,maxResults='50',pageToken=nextToken).execute()

        for playlist in response.get('items', []):
            playlists.append(playlist)

        nextToken = response.get('nextPageToken',-1)
        if( nextToken == -1 ):
            break;

    WriteLog ("Number of playlist : %d\n" % len(playlists))

    WriteLog ("Channel Title : %s\n" % playlists[0]['snippet']['channelTitle'])

    return playlists

