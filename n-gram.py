#/usr/bin/env python
# -*- coding: utf-8 -*-

#n-gramモデル学習プログラム
#http://www.phontron.com/slides/nlp-programming-ja-02-bigramlm.pdf

from math import *
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="help message")
parser.add_argument("-train", dest="train", default="/Users/kohei-mu/Downloads/nlptutorial/data/wiki-en-train.word",type=argparse.FileType('r'), help="training document")
parser.add_argument("-test", dest="test", default="/Users/kohei-mu/Downloads/nlptutorial/data/wiki-en-test.word", type=argparse.FileType("r"), help="test document")
args = parser.parse_args()

def train_ngram(train):
    counts = defaultdict(int)
    context = defaultdict(int)
    probability = {}
    for i in train:
        words = i.rstrip().split(" ")
        words.append("</s>")
        words.insert(0,"<s>")
        for l in xrange(0,len(words)):
            if l > 0:
                counts[words[l-1]+" "+words[l]] += 1
                context[words[l-1]] += 1
            counts[words[l]] += 1
            context[""] += 1
    for ngram, count in counts.items():
        con = ngram.split(" ")[0]
        try:
            probability[ngram] = float(counts[ngram]) / context[con]
        except:
            continue

    return probability, counts

def witten_bell(prob):
    dic = defaultdict(int)
    for word in prob:
        words = word.split()
        if words > 1:
            dic[words[0]] += 1
    return dic

def ngram_test(train, test):
    p, c = train_ngram(train)
    u_dic = witten_bell(p)
    w = 0
    h = 0
    for line in test:
        line = line.rstrip().split(" ")
        line.append("</s>")
        line.insert(0,"<s>")
        for l in xrange(1,len(line)-1):
            try:
                lambda_wi = 1 - float(u_dic[line[l-1]]) / (u_dic[line[l-1]] + c[line[l-1]])
                p_w = lambda_wi * p[line[l-1]+" "+line[l]] + (1 - lambda_wi) * p[line[l]]
                h += -log(p_w)
                w += 1
            except:
                continue
    return h/w

#実行
if __name__ == "__main__":
    print "entropy", ngram_test(args.train.readlines(), args.test.readlines())

