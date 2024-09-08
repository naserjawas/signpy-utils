"""
This file is for calculate summary of handtrackcleannew results.

author: naserjawas
date: 29 Jan 2024
"""

import csv
import glob
import argparse

from statistics import mean

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="This program tracks hand(s) in sign language video.")
    parser.add_argument("-p", "--path", help="path to the video", dest="path", required=True)
    args = parser.parse_args()

    dataset_path = args.path
    if dataset_path[-1] != "/":
        dataset_path += "/"
    print(dataset_path)
    file_path = dataset_path + "*.csv"
    filenames = sorted(glob.glob(file_path))
    print("Load", len(filenames), "csv files")

    grandd1 = []
    grandd2 = []
    grandhc = []
    framecounter = 0
    for filename in filenames:
        print(filename)
        with open(filename, newline="", mode="r") as csvfile:
            reader = csv.reader(csvfile)
            alld1 = []
            alld2 = []
            allhc = []
            counthc = 0
            oldfid = 0
            for row in reader:
                print(row)
                fid = int(row[0])
                hcx = int(row[1])
                hcy = int(row[2])
                d1 = float(row[3])
                d2 = float(row[4])
                alld1.append(d1)
                alld2.append(d2)
                grandd1.append(d1)
                grandd2.append(d2)
                if fid != oldfid and oldfid != 0:
                    allhc.append(counthc)
                    grandhc.append(counthc)
                    counthc = 0
                counthc += 1
                oldfid = fid
                framecounter += 1
            allhc.append(counthc)
            grandhc.append(counthc)
            if len(alld1) > 0:
                print("mean d1:", mean(alld1))
            else:
                print("mean d1: not available")
            if len(alld2) > 0:
                print("mean d2:", mean(alld2))
            else:
                print("mean d2: not available")
            if len(allhc) > 0:
                print("mean hc:", mean(allhc))
            else:
                print("mean hc: not available")
    if len(grandd1) > 0:
        print("grand mean d1:", mean(grandd1))
    else:
        print("grand mean d1: not available")
    if len(grandd2) > 0:
        print("grand mean d2:", mean(grandd2))
    else:
        print("grand mean d2: not available")
    if len(grandhc) > 0:
        print("grand mean hc:", mean(grandhc))
    else:
        print("grand mean hc: not available")
    print("frame counter:", framecounter)
