import glob
from xml.dom import minidom 
from WriteLog import WriteLog
import re
from lxml import html

def MdGenerator(dirname,mainCategory):

    # For screenshots

    pics_time = []
    pics_filename = []

    filelist = glob.glob("%s/%s/*.png" % ("contents/"+mainCategory,dirname))
    filelist = sorted(filelist)

    for file in filelist :
        pics_time.append(int(file[-14:-7]))
        pics_filename.append(file)

    # For subtitles

    sub_time = []
    sub_text = []       

    xmldoc = minidom.parse("contents/"+mainCategory+"/"+dirname+"/"+dirname+".xml")
    textlist = xmldoc.getElementsByTagName('text')
    
    for t in textlist :
        sub_time.append(int(float(t.attributes['start'].value)))
        sub_text.append(re.sub(r'[^\x00-\x7F]+','',re.sub(r"\n", r" ", t.firstChild.data)))

    # Export to .md

    WriteLog ("\t\t\tStart to write .md")

    f = open("contents/"+mainCategory+"/"+dirname+"/"+dirname+".md", 'w')

    f.write("# "+dirname)

    f.write("\n----\n\n")

    while not (len(pics_time) == 0 and len(sub_time) == 0) :

        if len(pics_time) == 0 :
            sub_time.pop(0)
            sub_text.pop(0)
            continue;

        if len(sub_time) == 0 :
            pics_time.pop(0)
            pics_filename.pop(0)
            continue;            

        if pics_time[0] <= sub_time[0] :
            f.write("\n\n![%s](./%s)\n\n" % (dirname,pics_filename[0]))
            pics_time.pop(0)
            pics_filename.pop(0)
        else :
            f.write("%s " % html.fromstring(sub_text[0]).text)
            sub_time.pop(0)
            sub_text.pop(0)

    f.close()

    return('finish')