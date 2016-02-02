#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
from math import tanh
from collections import defaultdict
from argparse import ArgumentParser
import pickle

def create_features(line):
	features = defaultdict(lambda: 0)
	words = line.strip().split(" ")
	for word in words:
		features["UNI:" + word] += 1
	return features

class Perceptron:

	_instance_num = int()
	_learning_late = 0.1

	def __init__(self):
		Perceptron._instance_num += 1
		self._id = Perceptron._instance_num
		self._weight = dict()
		self._delta = float()
		self._predict_result = float()

	def predict_one(self, features):

		#素性リストにない場合は初期化
		for key in features.keys():
			if not key in self._weight:
				self._weight[key] = random.uniform(-0.1, 0.1)

		score = 0

		#features: その層の各パーセプトロンの素性の集合
		#name:各パーセプトロンの識別番号
		#features{name:feature, name:feature, name:feature....}
		for name, feature in features.items():
			if name in self._weight:
				score += self._weight[name] * feature
				
		self._predict_result = tanh(score)
		return self._predict_result

	def update_delta(self, perceptron_list, true_label):

		#出力層の場合は正解ラベルと予測の比較
		if len(perceptron_list) == 0:
			self._delta = true_label - self._predict_result
		else:
			#出力層−１からエラーを伝搬し、tanhの勾配とともに計算
			sum = 0
			for each_percep in perceptron_list:
				#getWeight：その層の重みを取得
				sum += each_percep.getDelta() * each_percep.getWeight(self._id)

			self._delta = (1 - self._predict_result**2) * sum

	def update_weight(self, features):

		for key in features.keys():
			self._weight[key] += Perceptron._learning_late * self._delta * features[key]

	###便利関数
	def getWeight(self, key):
		#ここのkeyはニューラルネットの層を示している
		#_weight[key]はその層の重みを示す	
		return self._weight[key]
	#全体のパーゼプトロンのナンバーを返す
	#三層の場合。。。
	# [0]
	# 		[3]
	# [1]			[5]
	# 		[4]
	# [2]
	def getNeuralNum(self):
		return self._id
	def getPredictResult(self):
		return self._predict_result
	def getDelta(self):
		return self._delta

def main():

	parser = ArgumentParser(description="{0}[Args][Options]\n""Detailed options -h or --help".format(__file__))
	parser.add_argument("-i", "-iteration", type=int, dest="iteration", default=1, help="イテレーション回数")
	parser.add_argument("-l", "--layer", required=True, nargs="+", dest="layer", help="各層のパーゼプトロンの数、低い層から順に")
	parser.add_argument("-f" "--file", dest="file_name", help="入力ファイル名")
	args = parser.parse_args()

	nn = defaultdict(list)

	#ニューラルネットを張る（各層にパーセプトロンを張る）
	#layer:低い層から順に、各層のパーゼプトロンの数ex.4 3 2 1...
	#len(args.layer):張る層の数
	for num_of_perceptron, layer in zip(args.layer, range(len(args.layer))):
		for i in range(int(num_of_perceptron)):
			#各層の各パーセプトロンに対し、インスタンスを作る
			nn[layer].append(Perceptron())


	for line in open(args.file_name):

		true_label = int(line.split("\t")[0])
		string = line.split("\t")[1]
		#出力層を設定
		#last_perceptron = None

		for i in range(args.iteration):

			features_list = [create_features(string)]

			#予測
			#f_index:層のナンバーを示し、各層の素性を取りだす(features_list[f_index])
			#f_index-> ex.1,2,3,4..
			for layer, f_index in zip(nn.keys(), range(len(nn.keys()))):
				next_feature = dict()

				for perceptron in nn[layer]:
					perceptron.predict_one(features_list[f_index])
					next_feature[perceptron.getNeuralNum()] = perceptron.getPredictResult()
					#last_perceptron = perceptron

				features_list.append(next_feature)

			#逆伝搬
			for layer in reversed(nn.keys()):
				for perceptron in nn[layer]:
					perceptron.update_delta(nn[layer+1], true_label)
					#updateしたデルタでweightを再計算
					perceptron.update_weight(features_list[layer])

		pickle.dump(dict(nn), open("nn.dump", "wb"))

if __name__ == "__main__":
	main()

