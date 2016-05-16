from WriteLog import WriteLog
import GetPlaylists
import GetVideos
import Video2md
import urllib
import sys
import re
import os

def usage():
    print("""
Usage
=====
python %s [channelId]

ex)
python %s UCwRXb5dUK4cvsHbx-rGzSgw
""" % (sys.argv[0],sys.argv[0]))

if not sys.argv[1:]:
    usage()
else :
    cnt_deleted_video = 1
    cnt_no_subtitle = 1
    cnt_video = 1

    playlists = GetPlaylists.GetPlaylists(sys.argv[1])
    cnt1 = 1

    for playlist in playlists:
        WriteLog("\t%d. Playlist Title : %s" % (cnt1,playlist['snippet']['title']))
        cnt1 += 1

        mainCategory = re.sub(r" ", r"_", playlist['snippet']['title'])

        if not os.path.exists("contents/"+mainCategory):
            os.makedirs("contents/"+mainCategory)

        url_thumb = playlist['snippet']['thumbnails']['high']['url']
        WriteLog("\t\tStart to download a thumbnail image : %s" % url_thumb)
        urllib.urlretrieve(url_thumb, "contents/"+mainCategory+"/"+mainCategory+".jpg")

        videos = GetVideos.GetVideos(playlist['id'])
        cnt2 = 1

        for video in videos:
            WriteLog ("\t\t%d. Video Title : %s" % (cnt2,video['snippet']['title']))
            cnt2 += 1

            try:
                url_thumb = video['snippet']['thumbnails']['high']['url']
            except:
                WriteLog("\t\t\tDeleted Video. Skipped(%d)!!\n" % cnt_deleted_video)
                cnt_deleted_video += 1
                continue

            url = "https://www.youtube.com/watch?v="+video['snippet']['resourceId']['videoId']
            ret = Video2md.Video2md(url,mainCategory,url_thumb)

            if( ret == 'nosub' ):
                WriteLog ("\t\t\tFailed to download a subtitle!!(%d)\n\n" % cnt_no_subtitle)
                cnt_no_subtitle += 1
            elif( ret == 'done' ):
                WriteLog("\t\t\tDirectory has been detected. Skip this video!!(%d)\n" % cnt_video)
                cnt_video += 1
            elif( ret == 'finish' ):
                WriteLog("\t\t\tFinished!!(%d)\n" % cnt_video)
                cnt_video += 1

        WriteLog ("\n")

    WriteLog ("Finished!!!")
    WriteLog ("Total Videos : %d, Deleted : %d, No subtitle : %d" % (cnt_video,cnt_deleted_video,cnt_no_subtitle))