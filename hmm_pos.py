#/usr/bin/env python
# -*- coding: utf-8 -*-

#HMM品詞推定
#http://www.phontron.com/slides/nlp-programming-ja-05-hmm.pdf

#f = open("../../Downloads/nlptutorial/test/05-train-input.txt","r")
f = open("../../Downloads/nlp-programming/data/wiki-en-train.norm_pos","r")
w = open("pos_train.txt", "w")

def train(input_file):
	emit = {}
	transition = {}
	context = {}
	ganmma = 0.95
	N = 10**6
	for line in input_file:
		line = line.rstrip()
		previous = "<s>"
		if context.has_key("<s>"):
			context["<s>"] += 1
		else:
			context.setdefault("<s>",1)
		wordtags = line.split(" ")
		for wordtag in wordtags:
			wordtag = wordtag.split("_")
			word = wordtag[0]
			tag = wordtag[1]
			if transition.has_key(previous+" "+tag):
				transition[previous+" "+tag] += 1 
			else:
				transition.setdefault(previous+" "+tag, 1)
			if context.has_key(tag):
				context[tag] += 1
			else:
				context.setdefault(tag, 1)
			if emit.has_key(tag+" "+word):
				emit[tag+" "+word] += 1
			else:
				emit.setdefault(tag+" "+word, 1)
			previous = tag
		if transition.has_key(previous+" "+"</s>"):
			transition[previous+" "+"</s>"] += 1
		else:
			transition.setdefault(previous+" "+"</s>", 1)
	for key, value in transition.items():
		key = key.split(" ")
		previous = key[0]
		w.write("T" +" "+ " ".join(key) +" "+ str(float(value)/context[previous])+"\n")
	for key, value in emit.items():
		key = key.split(" ")
		tag = key[0]
		w.write("E" +" "+ " ".join(key) +" "+ str(ganmma * float(value)/context[tag] + (1-ganmma)/N)+"\n")


train(f)
