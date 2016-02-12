# _*_ coding: utf-8 _*_

#tf-idfの実装
#tf値 = その文書におけるある単語の総数 / その文書の単語の総出現回数
#idf値 = log( |文書の総数| / |ある単語を含む文書の総数| ) 

import MeCab, math, sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

#入力の文書
sentence = open(sys.argv[1], "r").readlines()

#文書の番号
sentence_num = len(sentence)
#文書のパーズ
tagger = MeCab.Tagger()
parsed = [tagger.parse(sentence[i]).decode("utf-8") for i in range(sentence_num)]

#文書ごとの単語リストを作成
wordList = [parsed[i].split()[:-1:2] for i in range(sentence_num)]

#文書ごとに単語ごとの出現回数をカウント
allCount = {}
wordCount = {}
for i in range(sentence_num):
	for word in wordList[i]:
		allCount[i] = wordCount.setdefault(word,0)
		wordCount[word] += 1
	#文書ごとの単語ごとの出現回数
	allCount[i] = wordCount
	#初期化	
	wordCount = {}

#文書ごとの単語の総出現回数をカウント
allWord = {}
sumCount = 0
for i in range(sentence_num):
    for word in allCount[i]:sumCount += allCount[i][word]
	#文書ごとの総出現回数	
    allWord[i] = sumCount
	#初期化
    sumCount = 0

#ある単語を含む文書の総数をカウント
allWordDoc = {}
for i in range(sentence_num):
	for word in wordList[i]:wordCount.setdefault(word,0)
	for word in allCount[i]:wordCount[word] += 1
	allWordDoc = wordCount

#tf値の計算
tfCount = {}
tf_score = {}
tfstore = {}
for i in range(sentence_num):
	#tf値 = その文書におけるある単語の総数 / その文書の単語の総出現回数
	for word in allCount[i]:tfCount[word] = allCount[i][word] * 1.0/allWord[i]
	#その文書の各々の単語のtf値をストア
	tfstore[i] = tfCount
	#初期化
	tfCount = {}

#idf値の計算
idfstore = {}
all_idf = {}
for i in range(sentence_num):
	#idf値 = log( |文書の総数| / |ある単語を含む文書の総数| ) 
	for word in allCount[i]:idfstore[word] = math.log(1.0 * math.fabs(sentence_num) / math.fabs(allWordDoc[word]))
	#文書ごとのidf値をストア
	all_idf[i] = idfstore
	#初期化
	idfstore = {}

#tf-idf値の計算
tfidf = {}
all_tfidf = {}
for i in range(sentence_num):
	#その文書のある単語ごとのtf-idf値を計算
	#tf-idf = tf * idf
    for word in allCount[i]:tfidf[word] = tfstore[i][word] * all_idf[i][word]
	#文書ごとにtf-idf値をストア
    all_tfidf[i] = tfidf
	#初期化
    tfidf = {}

#計算結果を出力
for i in range(sentence_num):
	for word, count in sorted(all_tfidf[i].items(), key = lambda x:x[1], reverse = True):
		print "text%d: %-16s %2.3f" %(i+1, word, count)


