#!/usr/bin/python
# encoding: utf-8

#単語分割
#http://www.phontron.com/slides/nlp-programming-ja-03-ws.pdf

import math, sys, argparse
from collections import defaultdict
reload(sys)
sys.setdefaultencoding("utf-8")

parser = argparse.ArgumentParser(description="help message")
parser.add_argument("-train", dest="train", default="/Users/kohei-mu/Downloads/nlptutorial/data/wiki-ja-train.word", type=argparse.FileType("r"), help="training document")
parser.add_argument("-test", dest="test", default="/Users/kohei-mu/Downloads/nlptutorial/data/wiki-ja-test.txt",type=argparse.FileType("r"), help="test documents")
args = parser.parse_args()

lamb1 = 0.95
lamb_unk = 1 - lamb1
V = 10 ** 6

def train_file(file):
    counts = defaultdict(lambda: 0)
    total = 0
    for line in file:
        words = line.strip().split(" ")
        words.append("</s>")
        for word in words:
            counts[word.decode("utf-8")] += 1
            total += 1
    
    probs = {}
    for word in counts.keys():
        probs[word] = counts[word] / float(total)
    model = {}
    model["probs"] = probs
    model["total"] = total

    return model

def calc_p(model, word):
	p = lamb_unk / V
	if word in model["probs"]:
		p += (lamb1 * model["probs"][word])
	return p

def is_in(model, word):
	return word in model["probs"].keys()

def split(model, line):
    line = line.strip()
    best_edge = defaultdict(lambda: None)
    best_score = defaultdict(lambda: 10 ** 10)
    best_score[0] = 0

    for word_end in range(1, len(line)):
        for word_begin in range(0, word_end):
            word = line[word_begin:word_end] 
            encoded = word.encode("utf-8")
            if len(word) == 1 or is_in(model, encoded):
                p = calc_p(model, encoded)
                score = best_score[word_begin] + (-math.log(p))
                if score < best_score[word_end]:
                    best_score[word_end] = score
                    best_edge[word_end] = (word_begin, word_end)

    words = []
    next_edge = best_edge[len(best_edge) - 1]
    while next_edge != None:
        word = line[next_edge[0]:next_edge[1]]
        encoded = word.encode("utf-8")
        words.append(encoded.strip())
        next_edge = best_edge[next_edge[0]]
    words.reverse()
    return " ".join(words)

def main():
    model = train_file(args.train.readlines())
    for line in args.test:
	    line = line.strip()
	    encoded = line.decode("utf-8")
	    splitted = split(model, encoded)
	    print splitted

if __name__  == "__main__":
    main()

