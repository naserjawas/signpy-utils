"""
This file cleans 'si' from the dataset, manually.

author: naserjawas
date: 16 December 2023
"""

import os
import glob

if __name__ == "__main__":
    sequencefile = "../dataset/RWTHPHOENIXWeather2014/phoenix2014-release/phoenix-2014-multisigner/annotations/automatic/train.alignment"
    sf = open(sequencefile, 'r')
    sflines = sf.readlines()

    dataloc = "../dataset/RWTHPHOENIXWeather2014/phoenix2014-release/phoenix-2014-multisigner/features/fullFrame-210x260px/train_no_si/"
    datadirs = os.listdir(dataloc)
    datadirs.remove(".DS_Store")
    print(datadirs)

    for line in sflines:
       l = line.split(" ")
       l_file = l[0].strip('\n')
       framedata = l_file.split("/")
       video = framedata[3]
       frameid = framedata[5].split("_")[-1][2:8]
       l_class = int(l[1])
       if video in datadirs and l_class == 3693:
            sifiles = sorted(glob.glob(dataloc + video + "/1/" + "*" + str(frameid) + "*"))
            for s in sifiles:
                print(s)
                os.remove(s)
            print()
