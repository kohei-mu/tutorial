#/usr/bin/env python
# -*- coding: utf-8 -*-

#パーセプトロン学習プログラム
#http://www.phontron.com/slides/nlp-programming-ja-03-perceptron.pdf

import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="help message")
parser.add_argument("-train", dest="train",default="/Users/kohei-mu/Downloads/nlptutorial/data/titles-en-train.labeled", type=argparse.FileType('r'),help="training document(labeled)")
parser.add_argument("-test", dest="test", default="/Users/kohei-mu/Downloads/nlptutorial/data/titles-en-test.word", type=argparse.FileType('r'), help="test document")
args = parser.parse_args()

#最初の重みを設定
def first_weights(lines):
    weight = defaultdict(int)
    for i in lines:
        i = i.strip().split("\t")
        words = i[1].split(" ")
        for word in words:
            word = "UNI: "+word
            weight[word] = 0
    return weight

#ユニグラムの素性を抽出 ../
def create_features(lines):
	phi = defaultdict(int)
	words = lines.strip().split(" ")
	for word in words:
		word = "UNI: "+word
		phi[word] += 1
	return phi

#一行ごとの重み付き和を計算し、予測
def predict_one(weight, phi):
	score = 0
	for name,value in phi.items():
		if name in weight:
			score += float(value) * weight[name]
	if score >= 0:
		return 1
	else:
		return -1

#重みの更新
def update_weights(weight,phi,y):
	for name,value in phi.items():
		if name in weight:
			weight[name] += int(value)*int(y)

#全体的な重みの学習
def learn(train):
    weight = first_weights(train)
    for i in train:
        i = i.rstrip().split("\t")
        y = i[0]
        x = i[1]
        phi = create_features(x)
        y_ = predict_one(weight,phi)
        if int(y_) != int(y):update_weights(weight,phi,y)

    return weight

#全体的な予測
def predict_all(train, test):
    weight = learn(train)
    for i in test:
        i = i.rstrip()
        phi = create_features(i)
        y_ = predict_one(weight,phi)
        if y_ == 1:
            print "POSITIVE :",i, "\n"
        else:
            print "NEGATIVE :",i, "\n"

if __name__ == "__main__":
    predict_all(args.train.readlines(), args.test.readlines())
