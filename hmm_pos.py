#/usr/bin/env python
# -*- coding: utf-8 -*-

#HMM品詞推定
#http://www.phontron.com/slides/nlp-programming-ja-05-hmm.pdf

from collections import defaultdict
import argparse, math

parser = argparse.ArgumentParser(description="help message")
parser.add_argument("-train",dest="train", default="/Users/kohei-mu/Downloads/nlptutorial/test/05-train-input.txt", type=argparse.FileType("r"), help="train document")
parser.add_argument("-test", dest="test", default="/Users/kohei-mu/Downloads/nlptutorial/test/05-test-input.txt", type=argparse.FileType("r"), help="test document")
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
                emit[wordTag[1]+" "+wordTag[0]] += 1
            if not pre_tag == "":
                trans[pre_tag+" "+wordTag[1]] += 1
            pre_tag = wordTag[1]
    emit_prob = defaultdict()
    trans_prob = defaultdict()
    for key, value in trans.items():
        trans_prob[key] = float(value) / tag_list[key.split()[0]]
    for key, value in emit.items():
        emit_prob[key] = _lambda * ( float(value) / tag_list[key.split()[0]] ) + (1 - _lambda)*1/N

    return emit_prob, trans_prob, tag_set

def backward_forward(test_doc, trans, emit, tags):
    for line in test_doc:
        words = line.strip().split()
        l = len(words)
        best_score = {}
        best_edge = {}
        best_score["0 <s>"] = 0
        best_edge["0 <s>"] = None
        for i in range(0, l):
            for prev_tag in tags:
                for next_tag in tags:
                    if best_score.has_key(str(i)+" "+prev_tag) and trans.has_key(prev_tag+" "+next_tag) and emit.has_key(next_tag+" "+words[i]):
                        score = best_score[str(i)+" "+prev_tag] - math.log(trans[prev_tag+" "+next_tag]) - math.log(emit[next_tag+" "+words[i]])
                        if ( not best_score.has_key(str(i+1)+" "+next_tag) ) or best_score[str(i+1)+" "+next_tag] > score:
                            best_score[str(i+1)+" "+next_tag] = score
                            best_edge[str(i+1)+" "+next_tag] = str(i)+" "+prev_tag
        for prev_tag in tags:
            if best_score.has_key(str(l)+" "+prev_tag) and trans.has_key(prev_tag+" "+"</s>"):
                score = best_score[str(l)+" "+prev_tag] - math.log(trans[prev_tag+" "+"</s>"])
                if (not best_score.has_key(str(l+1)+" "+"</s>")) or best_score[str(l+1)+" "+"</s>"] > score:
                    best_score[str(l+1)+" "+"</s>"] = score
                    best_edge[str(l+1)+" "+"</s>"] = str(l)+" "+prev_tag

        result_tags = []
        next_edge = best_edge[str(l+1)+" "+"</s>"]
        while next_edge != "0 <s>":
            position, tag = next_edge.split()
            result_tags.append(tag)
            next_edge = best_edge[next_edge]
        result_tags.reverse()
        print  " ".join(result_tags)


if __name__ == "__main__":
    emit, trans, tags = train(args.train)
    backward_forward(args.test, trans, emit, tags)
    
