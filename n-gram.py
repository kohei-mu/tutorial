#/usr/bin/env python
# -*- coding: utf-8 -*-

#n-gram学習プログラム
#http://www.phontron.com/slides/nlp-programming-ja-02-bigramlm.pdf

from math import *

#f = open("../Downloads/nlptutorial/test/02-train-input.txt","r").readlines()
f = open("../Downloads/nlptutorial/data/wiki-en-train.word","r").readlines()
test = open("../Downloads/nlptutorial/data/wiki-en-test.word","r").readlines()

def create_map(input):
	counts = {}
	context = {}
	probability = {}
	for i in input:
		i = i.rstrip()
		words = i.split(" ")
		words.append("</s>")
		words.insert(0,"<s>")
		for l in xrange(0,len(words)):
			if l > 0:
				if (words[l-1]+" "+words[l]) in counts:
					counts[words[l-1]+" "+words[l]] += 1
				else:
					counts[words[l-1]+" "+words[l]] = 1

				if words[l-1] in context:
					context[words[l-1]] += 1
				else:
					context[words[l-1]] = 1

		for h in xrange(0,len(words)):
			if words[h] in counts:
				counts[words[h]] += 1
			else:
				counts[words[h]] = 1

			if "" in context:
				context[""] += 1
			else:
				context[""] = 1


	for ngram, count in counts.items():
		con = ngram.split(" ")
		con = con[0]
		try:
			prob = float(counts[ngram])/context[con]
			probability[ngram] = prob

		except:
			continue

	return probability

def ngram_test(model_input, test_input):
	p = create_map(model_input)
	ganmma_1 = 0.9#補間係数
	ganmma_2 = 0.9#補間係数
	v = 1000000
	w = 0
	h = 0
	for line in test_input:
		line = line.rstrip()
		line = line.split(" ")
		line.append("</s>")
		line.insert(0,"<s>")
		for l in xrange(1,len(line)-1):
			try:
				p1 = ganmma_1 * p[line[l]] + (1 - ganmma_1) / v
				p2 = ganmma_2 * p[line[l-1]+" "+line[l]] + (1 - ganmma_2) * p1
				h += -log(p2)
				w += 1
			except:
				continue

	return h/w

#実行
print "entropy",ngram_test(f,test)

