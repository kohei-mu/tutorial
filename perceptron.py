#/usr/bin/env python
# -*- coding: utf-8 -*-

#パーセプトロン学習プログラム
#http://www.phontron.com/slides/nlp-programming-ja-03-perceptron.pdf

#f = open("../Downloads/nlptutorial/test/03-train-input.txt","r").readlines()
f = open("../Downloads/nlptutorial/data/titles-en-train.labeled","r").readlines()
j = open("../Downloads/nlptutorial/data/titles-en-test.word","r").readlines()

#最初の重みを設定
def first_weights(lines):
	weight = {}
	for i in lines:
		i = i.rstrip()
		i = i.split("\t")
		x = i[1]
		words = x.split(" ")
		for word in words:
			word = "UNI: "+word
			if word in weight:
				weight[word] += 0
			else:
				weight[word] = 0
	return weight

#ユニグラムの素性を抽出
def create_features(lines):
	phi = {}
	i = lines.rstrip()
	words = i.split(" ")
	for word in words:
		word = "UNI: "+word
		if word in phi:
			phi[word] += 1
		else:
			phi[word] = 1
	return phi

#一行ごとの重み付き和を計算し、予測
def predict_one(weight, phi):
	score = 0
	for name,value in phi.items():
		if name in weight:
			score += value * weight[name]
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
	for i in test:
		i = i.rstrip()
		phi = create_features(i)
		y_ = predict_one(weight,phi)
		print y_,i


#実行
predict_all(f,j)



