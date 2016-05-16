from WriteLog import WriteLog
import cv2
import cv
import numpy as np
import time
import os
 
def SceneChangeDetector(video_filename,dirname,mainCategory):
 
    cap = cv2.VideoCapture()
    cap.open(video_filename)
 
    if not cap.isOpened():
        WriteLog ("\nFatal error - could not open video %s." % video_filename)
        return
    else:
        WriteLog ("\t\t\tParsing video : %s..." % video_filename)
 
    width  = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    WriteLog ("\t\t\tVideo Resolution: %d x %d" % (width, height))

    selected_diffs = []
    selected_images = []
    selected_timestamps = []

    start_time = time.time()

    # For the first time     
    (rv, im) = cap.read()
    im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
    hist = cv2.calcHist([im], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist).flatten()
    last_change = -100
    last_frame = 0

    # Loop
    while True:

        prev_hist = hist
        prev_im = im

        (rv, im) = cap.read()
        if not rv:
            break

        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        frame_count = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        msec_count = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        if frame_count-last_frame == 30 :
            last_frame = frame_count

            im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
            hist = cv2.calcHist([im], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist).flatten()

            diff = cv2.compareHist(prev_hist,hist,cv.CV_COMP_CHISQR)
            if diff >= 0.5 :
                if frame_count-last_change > 600 :
                    last_change = frame_count
                    WriteLog ("\t\t\tDifference between %d and %d : %f" % (frame_count-1, frame_count, diff))
                    selected_timestamps.append(msec_count)
                    selected_images.append(prev_im)
                    selected_diffs.append(diff)
        else :
            continue

    frame_count = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)  # current capture position
    mins = int(frame_count / fps / 60)
    WriteLog ("\t\t\tRead %d mins(%d frames) from video." % (mins,frame_count))

    selected_ordered = sorted(zip(selected_diffs,selected_images,selected_timestamps),reverse = True)

    if( mins <= len(selected_ordered) ):
        cnt = mins
    else:
        cnt = len(selected_ordered)

    selected_ordered = selected_ordered[:cnt]

    for (diff,image,timestamp) in selected_ordered:
        out_filename = "%s/%s/%s_%010d.png" % ("contents/"+mainCategory,dirname,dirname,timestamp)
        cv2.imwrite(out_filename,image)
        WriteLog ("\t\t\tdifference : %f : %s" % (diff,out_filename))
 
    cap.release()

    elapsed_time = time.time() - start_time
    WriteLog ("\t\t\tElapsed time : %d sec" % elapsed_time)

    os.remove(video_filename)
