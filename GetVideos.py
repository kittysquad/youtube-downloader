from apiclient.discovery import build
from WriteLog import WriteLog

def GetVideos(pId):

    service = build('youtube', 'v3', developerKey = 'AIzaSyCuD-M96R2yX4d4o3UVFiBXwAdomxiog-w')

    nextToken = ''

    videos = []

    while True:
        response = service.playlistItems().list(part='snippet',playlistId=pId,maxResults='50',pageToken=nextToken).execute()

        for video in response.get('items', []):
            videos.append(video)

        nextToken = response.get('nextPageToken',-1)
        if( nextToken == -1 ):
            break;

    WriteLog ("\t\tNumber of videos : %d\n" % len(videos))

    return videos