from WriteLog import WriteLog
import urllib2
import re
import urllib
import os

def SubtitleExtractor(url,mainCategory,url_thumb):

    WriteLog("\t\t\tSource URL : %s" % url)
    try:    
        response = urllib2.urlopen(url)
        html = response.read()
    except:
        WriteLog("URL access error!")
        quit()

    title = re.search('<title>(.*?) - YouTube<\/title>', html)
    title = title.group(1)
    title = re.sub(r" ", r"_", title)
    code = url[-11:]
    filename = title

    if os.path.exists("contents/"+mainCategory+"/"+filename+"/"+filename+".md"):
        return('done')

    if not os.path.exists("contents/"+mainCategory+"/"+filename):
        os.makedirs("contents/"+mainCategory+"/"+filename)
        
    try:
        url = re.search('\'TTS_URL\': "(.*?)"', html)
        url = url.group(1)
        if( len(url) < 5 ):
            return('nosub')
        url = re.sub(r"\\/", r"/", url)
        url = re.sub(r"\\u0026", r"&", url)
        url = urllib.unquote(url).decode('utf8') + "&type=track&lang=en&name&kind=asr&fmt=1"
        response = urllib2.urlopen(url)
        html = response.read()
        if( len(html) == 0 ):
            return('nosub')
    except:
        return('nosub')

    WriteLog("\t\t\tStart to download a thumbnail image : %s" % url_thumb)
    urllib.urlretrieve(url_thumb, "contents/"+mainCategory+"/"+filename+"/"+filename+".jpg")

    WriteLog("\t\t\tStart to write a file : %s" % ("contents/"+mainCategory+"/"+filename+"/"+filename+".xml"))
    response = urllib2.urlopen(url)
    html = response.read()
    f = open("contents/"+mainCategory+"/"+filename+"/"+filename+".xml", 'w')
    f.write(html)
    f.close()

    return(filename)
