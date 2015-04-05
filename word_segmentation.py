#!/usr/bin/python
# encoding: utf-8

#word segmentation

import math
from collections import defaultdict

lamb1 = 0.95
lamb_unk = 1 - lamb1
V = 10 ** 6

#unigram training
def train_file(filename):
	infile = open(filename, "r")
	counts = defaultdict(lambda: 0)
	total = 0
	for line in infile:
		line = line.rstrip()
		words = line.split(" ")
		words.append("</s>")
		for word in words:
			counts[word] += 1
			total += 1
	probs = {}
	for word in counts:
		probs[word] = counts[words] / float(total)
	model = {}
	model["probs"] = probs
	model["total"] = total
	return model

#calculate the weight of the edge
def calc_p(model, word):
	p = lamb_unk / V
	if word in model["probs"]:
		p += (lamb1 * model["probs"][word])
	return p

#whether "the word" is  in the model
def is_in(model, word):
	return word in model["probs"]


#split the words
def split(model, line):
	best_edge = defaultdict(lambda: None)
	best_score = defaultdict(lambda: 10 ** 10)
	best_score[0] = 0

	#forward
	for word_end in range(1, len(line)):
		for word_begin in range(0, word_end - 1):
			word = line[word_begin:word_end]
			encoded = word.encode("utf-8")
			if len(word) == 1 or is_in(model, encoded):
				#the weight of the edge
				p = calc_p(model, encoded)
				#calculate the score
				score = best_score[word_begin] + (-math.log(p))
				if score < best_score[word_end]:
					#update the score
					best_score[word_end] = score
					#update the best_edge
					best_edge[word_end] = (word_begin, word_end)

	#backward
	words = []
	next_edge = best_edge[len(best_edge) - 1]
	while next_edge != None:
		word = line[next_edge[0]:next_edge[1]]
		encoded = word.encode("utf-8")
		words.append(encoded)
		next_edge = best_edge[next_edge[0]]
	words.reverse()
	#return the splitted words
	return " ".join(words)


#############execute###################

#train uni gram model
model = train_file("infile_for_uni_gram")
test_file = open("infile_for_test","r")
for line in test_file:
	line = line.rstrip()
	encoded = unicode(line, "utf-8")
	splitted = split(model, encoded)
	print splitted



######動作未確認


