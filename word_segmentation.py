#!/usr/bin/python
# encoding: utf-8

input = open("/Users/kohei-mu/Downloads/kftt-data-1.0/data/tok/train.ja","r")
input_for_split = open("/Users/kohei-mu/Downloads/nlptutorial/data/wiki-ja-test.txt","r")

#word segmentation

import math
from collections import defaultdict

lamb1 = 0.95
lamb_unk = 1 - lamb1
V = 10 ** 6

#unigram training
def train_file(file):
	counts = defaultdict(lambda: 0)
	total = 0 #total of words

	for line in file:
		words = line.strip().split(" ")
		words.append("</s>")
		for word in words:
			counts[word] += 1 #number of each words
			total += 1 #total of words
	
	probs = {} #unigram features
	for word in counts.keys():
		probs[word] = counts[word] / float(total)
	
	model = {}
	#model:  {probs{word:uni}, total of words}
	model["probs"] = probs
	model["total"] = total
	return model

#calculate the unigram for unk word
def calc_p(model, word):
	#p = lambda * unigram + ( (1-lamda) / V(big number) )
	p = lamb_unk / V
	if word in model["probs"]:
		p += (lamb1 * model["probs"][word])
	return p

#return whether or not the word is in the model dic
def is_in(model, word):
	return word in model["probs"].keys()


#split the words with viterbi
#forward and backward algorithm
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
				#best_score[word_begin]: next score
				score = best_score[word_begin] + (-math.log(p))
				#best_score[word_end]: (previous) next score
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
		words.append(encoded.strip())
		next_edge = best_edge[next_edge[0]]
	words.reverse()
	#return the splitted words
	return " ".join(words)


#############execute###################

model = train_file(input)
for line in input_for_split:
	line = line.strip()
	encoded = line.decode("utf-8")
	splitted = split(model, encoded)
	print splitted
