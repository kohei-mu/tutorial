#/usr/bin/env python
# -*- coding: utf-8 -*-

#readlines()daiji
f = open("../../Downloads/nlptutorial/data/titles-en-train.labeled","r").readlines()
j = open("../../Downloads/nlptutorial/data/titles-en-test.word","r").readlines()

from collections import defaultdict
import math

#最初の重みを設定
def first_weights(lines):
    weight = defaultdict(int)
    for i in lines:
        i = i.strip().split("\t")
        words = i[1].split(" ")
        for word in words:
            word = "UNI: " + word
            weight[word] = 0
    return weight

#ユニグラムの素性を抽出
def create_features(lines):
	phi = defaultdict(int)
	words = lines.strip().split(" ")
	for word in words:
		word = "UNI: " + word
		phi[word] += 1
	return phi

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
def update_weights(weight,phi,y,c):
    for name,value in weight.items():
        if abs(value) < c:
            weight[name] = 0
        else:
            weight[name] -= predict_one(weight, phi)  * c
    for name, value in phi.items():
    	weight[name] += float(value) * y

#全体的な重みの学習
#margin:マージン
#c:正則化定数
def learn(input,margin,c):
    weight = first_weights(input)
    for i in input:
        x = i.strip().split("\t")[1]
        y = int(i.strip().split("\t")[0])
        phi = create_features(x)
        if sum(weight[name] * phi[name] for name in phi.keys()) * y <= margin:
            update_weights(weight,phi,y,c)
    return weight

#全体的な予測
def predict_all(input, test):
    weight = learn(input,0.1, 0.0001)
    #print weight
    for i in test:
        i = i.strip()
        phi = create_features(i)
        y_ = predict_one(weight,phi)
        print y_,i

#実行
predict_all(f,j)
