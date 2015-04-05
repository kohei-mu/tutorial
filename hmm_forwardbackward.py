#/usr/bin/env python
# -*- coding: utf-8 -*-

#HMM品詞推定
#http://www.phontron.com/slides/nlp-programming-ja-05-hmm.pdf
import math

k = open("pos_train.txt","r")
j = open("../../Downloads/nlp-programming/data/wiki-en-test.norm","r")

transition = {}
emission = {}
possible_tags = {}

for line in k:
	line = line.split(" ")
	type = line[0]
	context = str(line[1])
	word = str(line[2])
	prob = line[3].rstrip()
	possible_tags.setdefault(context, 1)
	if type == "T":
		transition.setdefault(context+" "+word, float(prob))
	elif type == "E":
		emission.setdefault(context+" "+word, float(prob))

list = possible_tags.keys()
sentence = "Natural language processing ( NLP ) is a field of computer science"
words = sentence.split(" ")
l = len(words)
best_score = {}
best_edge = {}
best_score.setdefault("0 <s>", 0)
best_edge.setdefault("0 <s>", None)


for i in range(0,(l-1)):
	for prev in list:
		for next in list:
			if best_score.has_key(str(i)+" "+str(prev)) and transition.has_key(str(prev)+" "+str(next)):
				try:
 					score = best_score[str(i)+" "+str(prev)] +(- math.log(transition[str(prev)+" "+str(next)])) + (- math.log(emission[str(next)+" "+words[i]]))	
 					
 					if not best_score.has_key(str(i+1)+" "+str(next)):
 						best_score[str(i+1)+" "+str(next)] = score
 						best_edge[str(i+1)+" "+str(next)] = str(i)+" "+str(prev)
 					elif best_score[str(i+1)+" "+str(next)] > score:
 						best_score[str(i+1)+" "+str(next)] = score
 						best_edge[str(i+1)+" "+str(next)] = str(i)+" "+str(prev)
 					print i
 				except:
 					continue

 		


print best_edge
print "\n"
print best_score










# for line in j:
# 	words = line.split(" ")
# 	l = len(words)
# 	best_score = {}
# 	best_edge = {}

# 	best_score.setdefault("0 <s>", 0)
# 	best_edge.setdefault("0 <s>", None)


# 	for i in xrange(0,(l-1)):
# 		for prev in list:
# 			for next in list:
# 				if best_score.has_key(str(i)+" "+str(prev)) and transition.has_key(str(prev)+" "+str(next)) and emission.has_key(str(next)+" "+words[i]):
# 					score = best_score[str(i)+" "+str(prev)] +(- math.log(transition[str(prev)+" "+str(next)])) + (- math.log(emission[str(next)+" "+words[i]]))
					
					
# 					if not best_score.has_key(str(i+1)+" "+str(next)):
# 						best_score[str(i+1)+" "+str(next)] = score
# 						best_edge[str(i+1)+" "+str(next)] = str(i)+" "+str(prev)
# 					elif best_score[str(i+1)+" "+str(next)] > score:
# 						best_score[str(i+1)+" "+str(next)] = score
# 						best_edge[str(i+1)+" "+str(next)] = str(i)+" "+str(prev)



# 	best_score.setdefault(str(l)+" "+"</s>", 0)
# 	for j in xrange(l,(l+1)):
# 		for next in list:
# 			if best_score.has_key(str(j)+" "+"</s>") and transition.has_key(str(next)+" "+"</s>"):
# 				score = best_score[str(j)+" "+"</s>"] - math.log(transition[str(next)+" "+"</s>"]) 

# 				if not best_score.has_key(str(j+1)+" "+"</s>") or best_score[str(j+1)+" "+"</s>"] > score:
#  						best_score[str(j)+" "+"</s>"] = score
#  						best_edge[str(j)+" "+"</s>"] = str(j)+" "+str(next)

#  	print str(best_score)+"\n"+str(best_edge)
# 	tags = []
# 	next_edge = {}
# 	print best_edge[str(l)+" "+"</s>"]

# 	while next_edge != "0 <s>":
# 		edge = next_edge.split(" ")
# 		position = edge[0]
# 		tag = edge[1]
# 		tags.append(tag)

# 		#next_edge = best_edge[next_edge]
# 		break
# 	tags.reverse()
# 	#print str(best_score)+"\n"+str(best_edge)
# 	#print tags
# 	break







