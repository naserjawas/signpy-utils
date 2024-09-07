"""
This file breaks a video of BOBSL into sentences.

author: naserjawas
date: 14 October 2023
"""

import os
import shutil
import cv2 as cv
import math
import argparse
from datetime import datetime, timedelta

def extract_frame_number(time, framerate):
    td = timedelta(hours=time.hour,
                   minutes=time.minute,
                   seconds=time.second,
                   microseconds=time.microsecond)
    framenumber = math.floor(td.total_seconds() * framerate)

    return framenumber


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="This program breaks a BOBSL video frames into separate sentences.")
    parser.add_argument("-v", "--video", help="video videonumber", dest="videonumber", required=True)
    args = parser.parse_args()
    print("videonumber:", args.videonumber)

    videonumber = args.videonumber
    # root = "/storage/eng/esrsts/dataset/BOBSL/bobsl"
    root = "../dataset/BOBSL/bobsl"
    videoname = root + "/videos/" + videonumber + ".mp4"
    if not os.path.exists(videoname):
        print("Video file not found")
        exit()

    subtitle = root + "/subtitles/manually-aligned/" + videonumber + ".vtt"
    if not os.path.exists(subtitle):
        print("Subtitle file not found")
        exit()

    # extract video into frame.
    framedir = root + "/videos/" + videonumber + "/"
    if not os.path.exists(framedir):
        os.mkdir(framedir)

    videoframes = []
    v = cv.VideoCapture(videoname)
    framerate = v.get(cv.CAP_PROP_FPS)
    i = 0
    while(v.isOpened()):
        ret, frm = v.read()
        if not ret:
            break

        framenumber = str(i).zfill(12)
        framename = root + "/videos/" + videonumber + "/" + framenumber + ".png"
        cv.imwrite(framename, frm)
        print(framenumber, "is saved.")
        i += 1
        videoframes.append(framename)
    v.release()
    print("Reading and writing video frames finished...")

    # extract sentences from subtitle.
    with open(subtitle, 'r') as f:
        subtitleline = f.readlines()
    f.close()

    # create folder
    targetdir = root + "/videos/" + videonumber + "s/"
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)

    sentencenumber = 0
    foundtime = False
    for i, line in enumerate(subtitleline):
        line = line.strip()
        if line != "\n":
            if line[0:2].isnumeric() and line[2] == ":" and line[3:5].isnumeric():
                times = line.split(" --> ")
                starttime = datetime.strptime(times[0], "%H:%M:%S.%f").time()
                stoptime = datetime.strptime(times[1], "%H:%M:%S.%f").time()
                startframe = extract_frame_number(starttime, framerate)
                stopframe = extract_frame_number(stoptime, framerate)
                # print(startframe, stopframe)
                sentenceframes = videoframes[startframe:stopframe+1]
                sentencedir = targetdir + str(sentencenumber) + "/"
                if not os.path.exists(sentencedir):
                    os.makedirs(sentencedir)
                for sf in sentenceframes:
                    shutil.copy2(sf, sentencedir)

                sentencenumber += 1
                foundtime = True
            elif foundtime:
                # print(line)
                foundtime = False
            else:
                continue

    print("deleting framedir and its contents...")
    shutil.rmtree(framedir)
