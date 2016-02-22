#/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description="help message")
parser.add_argument("-train", dest="train", default="/Users/kohei-mu/Downloads/nlptutorial/data/titles-en-train.labeled",type=argparse.FileType("r"), help="train document")
parser.add_argument("-test", dest="test", default="/Users/kohei-mu/Downloads/nlptutorial/data/titles-en-test.word", type=argparse.FileType("r"), help="test document")
args = parser.parse_args()

def first_weights(lines):
    weight = defaultdict(int)
    for i in lines:
        i = i.strip().split("\t")
        words = i[1].split()
        for word in words:
            word = "UNI: " + word
            weight[word] = 0
    return weight

def create_features(lines):
	phi = defaultdict(int)
	words = lines.strip().split()
	for word in words:
		word = "UNI: " + word
		phi[word] += 1
	return phi

def predict_one(weight, phi):
    score = 0
    for name,value in phi.items():
        if name in weight:
            score += float(value) * weight[name]
    return 1 if score >= 0 else -1

def update_weights(weight, phi, y, c):
    for name,value in weight.items():
        if abs(value) < c:
            weight[name] = 0
        else:
            weight[name] -= value/abs(value) * c
    for name, value in phi.items():
    	weight[name] += float(value) * y

def learn(train, margin, c):
    weight = first_weights(train)
    for i in train:
        i = i.strip().split("\t")
        x = i[1]
        y = int(i[0])
        phi = create_features(x)
        if sum(weight[name] * phi[name] for name in phi.keys()) * y <= margin:
            update_weights(weight, phi, y, c)
    return weight

def predict_all(train, test):
    weight = learn(train, 0.1, 0.0001)
    for i in test:
        i = i.strip()
        phi = create_features(i)
        y_ = predict_one(weight,phi)
        if y_ == 1:
            print "POSITIVE :",i, "\n"
        else:
            print "NEGATIVE :",i, "\n"

if __name__ == "__main__":
    predict_all(args.train.readlines(), args.test.readlines())

