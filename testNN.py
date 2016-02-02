#/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
from math import tanh
from collections import defaultdict
from argparse import ArgumentParser
import pickle
from trainNN import *

def signDef(num):

	if num >= 0:
		return 1
	else:
		return -1

def create_features(string):

	features = defaultdict(lambda: 0)
	words = string.split(" ")

	for word in words:
		features["UNI:"+word] += 1

	return features

def main():

	parser = ArgumentParser("{0} [Args] [Options]\n""Detailed options -h or --help")
	parser.add_argument("-n","--nn",required=True, dest="nn_file", help="学習済みのネットワーク名")
	parser.add_argument("-f","--file", required=True, dest="file_name", help="テストファイル名")
	args = parser.parse_args()

	nn = pickle.load(open(args.nn_file))

	for line in open(args.file_name):

		last_perceptron = None
		features_list = [create_features(line.strip())]

		for layer, f_index in zip(nn.keys(), range(len(nn.keys()))):
			next_feature = dict()

			for perceptron in nn[layer]:
				perceptron.predict_one(features_list[f_index])
				next_feature[perceptron.getNeuralNum()] = perceptron.getPredictResult()
				last_perceptron = perceptron
			features_list.append(next_feature)

		print signDef(last_perceptron.getPredictResult()), line


if __name__=="__main__":
	main()

