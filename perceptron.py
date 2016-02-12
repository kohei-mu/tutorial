#/usr/bin/env python
# -*- coding: utf-8 -*-

#パーセプトロン学習プログラム
#http://www.phontron.com/slides/nlp-programming-ja-03-perceptron.pdf

f = open("../../Downloads/nlptutorial/data/titles-en-train.labeled","r").readlines()
j = open("../../Downloads/nlptutorial/data/titles-en-test.word","r").readlines()
from collections import defaultdict
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

#ユニグラムの素性を抽出c ../
def create_features(lines):
	#phi = {}
	phi = defaultdict(int)
	#i = lines.strip()
	#words = i.split(" ")
	words = lines.strip().split(" ")
	for word in words:
		word = "UNI: "+word
		phi[word] += 1
	return phi

#def create_features_(lines):
#    phi = defaultdict(int)
#    counts = defaultdict(int)
#    total_count = 0

#    words = lines.strip().split(" ")
#    for word in words:
#        word = "UNI: " + word
#        counts[word] += 1
#        total_count += 1
#    for word in words:
#        word = "UNI: " + word
#        phi[word] = float(counts[word]) / total_count
#    return phi

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
def learn(input):
	weight = first_weights(input)
	for i in input:
		i = i.rstrip()
		i = i.split("\t")
		y = i[0]
		x = i[1]
		phi = create_features(x)
		y_ = predict_one(weight,phi)
		if int(y_) != int(y):
			update_weights(weight,phi,y)

	return weight


#全体的な予測
def predict_all(input, test):
	weight = learn(input)
	print weight
	for i in test:
		i = i.rstrip()
		phi = create_features(i)
		#print phi
		y_ = predict_one(weight,phi)
		#print y_,i


#実行
predict_all(f,j)
