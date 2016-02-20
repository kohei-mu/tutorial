#/usr/bin/env python
# -*- coding: utf-8 -*-

#HMM品詞推定
#http://www.phontron.com/slides/nlp-programming-ja-05-hmm.pdf

from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description="help message")
parser.add_argument("-train",dest="train", default="/Users/kohei-mu/Downloads/nlp-programming/data/wiki-en-train.norm_pos", type=argparse.FileType("r"), help="train document")
parser.add_argument("-test", dest="test", default="/Users/kohei-mu/Downloads/nlp-programming/data/wiki-en-test.norm", type=argparse.FileType("r"), help="test document")
args = parser.parse_args()


def train(train_doc):
    emit = defaultdict(int)
    trans = defaultdict(int)
    tag_list = defaultdict(int)
    tag_set = set()
    _lambda = 0.95
    N = 10 ** 6
    for line in train_doc:
        words = line.strip().split()
        words.insert(0, "<s>_<s>")
        words.append("</s>_</s>")
        pre_tag = ""
        for word in words:
            wordTag = word.split("_")
            tag_list[wordTag[1]] += 1
            tag_set.add(wordTag[1])
            if word is not "<s>_<s>" and word is not "</s>_</s>":
                trans[wordTag[1]+" "+wordTag[0]] += 1
            if not pre_tag == "":
                emit[pre_tag+" "+wordTag[1]] += 1
            pre_tag = wordTag[1]
    emit_prob = defaultdict()
    trans_prob = defaultdict()
    for key, value in emit.items():
        emit_prob[key] = float(value) / tag_list[key.split()[0]]
    for key, value in trans.items():
        trans_prob[key] = _lambda * ( float(value) / tag_list[key.split()[0]] ) + (1 - _lambda)*1/N

    return emit_prob, trans_prob, tag_set



a,b, c = train(args.train)
