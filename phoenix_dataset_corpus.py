"""
This file processes the Phoenix dataset corpus and finds the similar
words across the train, test and dev set.

author: naserjawas
date: 17 August 2024
"""

import os

def loadtextfiles(rootdir, filename):
    lines = []
    if os.path.exists(rootdir + filename):
        print(f"{filename} corpus is found...")
        with open(rootdir + filename, "r") as pf:
            lines = pf.readlines()
        pf.close()
    print(f"length {filename}: {len(lines)}")

    return lines

def getwords(lines):
    filenames = []
    words = []
    for l in lines:
        l0 = str(l).split("|")
        l1 = l0[-1].split(" ")
        l1[-1] = l1[-1].strip()
        l2 = l0[0]
        filenames.append(l2)
        words.append(l1)

    return filenames, words

if __name__ == "__main__":
    drive = "../dataset/RWTHPHOENIXWeather2014"
    rootdir = drive + "/phoenix2014-release/phoenix-2014-multisigner/annotations/manual/"

    trainfile = loadtextfiles(rootdir, "train")
    testfile = loadtextfiles(rootdir, "test")
    devfile = loadtextfiles(rootdir, "dev")

    trainfilenames, trainwords = getwords(trainfile)
    testfilenames, testwords = getwords(testfile)
    devfilenames, devwords = getwords(devfile)

    maxcount = 0
    for i, w0 in enumerate(trainwords):
        count = 0
        filenames = []
        for j, w1 in enumerate(testwords):
            match = []
            for w in w0:
                if w in w1 and w not in match:
                    match.append(w)
            ratio = len(match) / len(w1)
            if ratio >= 0.75:
                # print(match, ratio)
                count += 1
                filenames.append((testfilenames[j], w1))
        if count > maxcount:
            maxcount = count
            print(f"{trainfilenames[i]} has {count}\n{w0} ")
            for f in filenames:
                print(f"- {f[0]}\n  {f[1]}")
