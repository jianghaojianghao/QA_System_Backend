# JiangHao

import nltk

sentence = "who is the father of Xiaoming"
words = nltk.word_tokenize(sentence)
tags = nltk.pos_tag(words) # 词性识别
ners = nltk.ne_chunk(tags, binary=False) # 实体识别
print(tags)
print(ners)


