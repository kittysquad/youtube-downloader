from __future__ import unicode_literals
from WriteLog import WriteLog
import SubtitleExtractor
import SceneChangeDetector
import MdGenerator
import youtube_dl

def my_hook(d):

    if d['status'] == 'finished':
        global video_filename
        video_filename = d['filename']
        WriteLog ("\t\t\tDownload completed : %s" % video_filename)

def Video2md(url,mainCategory,url_thumb):

    ret = SubtitleExtractor.SubtitleExtractor(url,mainCategory,url_thumb)
    if ( ret == 'nosub' ) or ( ret == 'done' ):
        return(ret)

    ydl_opts = {
        'progress_hooks': [my_hook],
        'quiet': True
    }

    WriteLog ("\t\t\tStart to download a Youtube video")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url]) 
        except:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    SceneChangeDetector.SceneChangeDetector(video_filename,ret,mainCategory)

    ret = MdGenerator.MdGenerator(ret,mainCategory)

    return(ret)

