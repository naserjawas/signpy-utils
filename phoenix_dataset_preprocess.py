"""
This file pre-process the dataset to change its form from single line per frame
to summary of the occurance of sign word.

author: naserjawas
date  : 14 November 2023
"""

import os

if __name__ == "__main__":
    sequencefile = "../dataset/RWTHPHOENIXWeather2014/phoenix2014-release/phoenix-2014-multisigner/annotations/automatic/train.alignment"
    classfile = "../dataset/RWTHPHOENIXWeather2014/phoenix2014-release/phoenix-2014-multisigner/annotations/automatic/trainingClasses.txt"
    cf = open(classfile, 'r')
    cflines = cf.readlines()
    cflines.pop(0)

    classdict = {}
    for line in cflines:
        l = line.split(" ")
        l_id = int(l[1])
        l_class = l[0]
        classdict[l_id] = l_class

    sf = open(sequencefile, 'r')
    sflines = sf.readlines()

    start = 0
    oldframeid = 0
    oldvideo = ""
    oldclassname = ""
    for line in sflines:
        l = line.split(" ")
        l_file = l[0].strip('\n')
        framedata = l_file.split("/")
        video = framedata[3]
        frameid = int(framedata[5].split("_")[-1][2:8])
        l_class = int(l[1])
        l_classname = classdict[l_class]

        if l_classname[-1].isnumeric():
            l_classname = l_classname[:-1]

        if oldvideo != video:
            if oldclassname != "":
                print(f"{oldclassname}: {start}-{oldframeid}")
            start = 0
            print(f"\n{video}:")
        elif oldclassname != l_classname :
            print(f"{oldclassname}: {start}-{oldframeid}")
            start = frameid

        # print(video, frameid, l_classname)

        oldvideo = video
        oldclassname = l_classname
        oldframeid = frameid

    print(f"{oldclassname}: {start}-{frameid}")
