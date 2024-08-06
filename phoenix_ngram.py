"""
This file is used to generate the n-gram data from Phoenix dataset.

author: naserjawas
date: 14 December 2023
"""

import os
import csv
import pickle
import argparse

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="This script parses phoenix sentences into ngram data.")
    parser.add_argument("-f", "--file", help="corpus file.", dest="corpusfile", required=True)
    parser.add_argument("-n", "--ngram", help="number of ngram.", dest="n", required=True)
    args = parser.parse_args()

    # get the arguments
    corpusfile = args.corpusfile
    n = args.n

    sentences = []
    with open(corpusfile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentence = row['id|folder|signer|annotation'].split('|')[-1]
            sentences.append(sentence)
    csvfile.close()
    print(f"{len(sentences)} sentences loaded...")

    ngram = []

    for sentence in sentences:
        words = sentence.split(" ")
        for i in range(len(words) - (n-1)):
            ngram.append(words[i:i+n])

    with open(f"phoenix_{n}grams", "wb") as pf:
        pickle.dump(ngram, pf)
    pf.close()

    print("ngrams file saved...")