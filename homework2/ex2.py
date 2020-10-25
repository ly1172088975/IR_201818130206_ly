# -*- coding:utf8 -*
import re
import json
import codecs
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import math

punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
re_punctuation = "[{}]+".format(punctuation)

'''
f = open("C:/Users/11720/Desktop/IR&DM/EX/E1/tweets.txt", "r", encoding = "utf-8")
f1 = codecs.open("C:/Users/11720/Desktop/IR&DM/EX/E2/dict.txt", "w", encoding = "utf-8")
f2 = codecs.open("C:/Users/11720/Desktop/IR&DM/EX/E2/cnt.txt", "w", encoding = "utf-8")
text_set = {}       #每篇test的内容
id_set = {}         #每篇test的id
i = 0
for lines in f.readlines():
    i += 1
    data = json.loads(lines)
    text_set[i] = data['text']
    id_set[i] = data['tweetId']
    #print(data)
f.close()

#print(id_set)
#print(re_punctuation)
dic = {}
for j in range(1,len(text_set)+1):
    content = text_set[j]
    content = content.lower()
    content = re.sub(re_punctuation, "", content)
    words = word_tokenize(content)
    w_list = []
    for w in words:
        #w1 = WordNetLemmatizer().lemmatize(w, pos="n")
        w2 = WordNetLemmatizer().lemmatize(w, pos="v")
        w3 = WordNetLemmatizer().lemmatize(w2, pos="a")
        w_list.append(w3)
    f2.write(id_set[j] + ':' + str(len(w_list)) + '\n')
    for w in w_list:
        if w not in dic:
            #当前索引字典中不存在这个词项
            dic[w] = dict()
            dic[w][id_set[j]] = 1
        else:
            if id_set[j] not in dic[w]:
                dic[w][id_set[j]] = 1
            else:
                dic[w][id_set[j]] += 1
f2.close()

word_list = dic.items()
sorted(word_list)

for w, id in word_list:
    if len(dic[w]) > 2 :     #词频过低的直接忽略
        f1.write(w + ':' + str(len(dic[w])) + '\n')
        word_list1 = id.items()
        sorted(word_list1, key=lambda x: x[0], reverse=True)
        for k, v in word_list1:
            f1.write(k + ":" + str(v) + "\n")
            #f1.write(str(k) + ":" + str(v) + "\n")
f1.close()
print("dict is ready.")
'''

f = open("C:/Users/11720/Desktop/IR&DM/EX/E1/tweets.txt", "r", encoding = "utf-8")
f1 = open("C:/Users/11720/Desktop/IR&DM/EX/E2/dict.txt", "r", encoding="utf-8")
f2 = open("C:/Users/11720/Desktop/IR&DM/EX/E2/cnt.txt", "r", encoding="utf-8")
N = 0
id_set = {}
for lines in f.readlines():
    N += 1
    data = json.loads(lines)
    id_set[N] = data['tweetId']
f.close()

tf = {}
df = {}
idf = {}
l = []
flag = 0
w = ""
n = 0
k = 0
for lines in f1.readlines():
    if flag == 0:
        w = lines.split(':')[0]
        n=int(lines.split(':')[1])
        df[w] = n
        idf[w] = math.log10(N/n)
        tf[w] = {}
        flag = 1
    else:
        id = lines.split(':')[0]
        t = int(lines.split(':')[1])
        tf[w][id] = 1 + math.log10(t)
        k += 1
        if k == n:
            flag = 0
            k = 0
f1.close()

length = {}
for lines in f2.readlines():
    id = lines.split(':')[0]
    cnt = lines.split(':')[1]
    length[id] = int(cnt)
f2.close()

K = 10
while True:
    print("please input your query:")
    q = input()
    if q == '':
        break
    q = q.lower()
    q = re.sub(re_punctuation, "", q)
    q = word_tokenize(q)
    q_list = []
    for w in q:
        #w1 = WordNetLemmatizer().lemmatize(w, pos="n")
        w2 = WordNetLemmatizer().lemmatize(w, pos="v")
        w3 = WordNetLemmatizer().lemmatize(w2, pos="a")
        q_list.append(w3)
    #print(q_list)
    ans = {}
    for i in id_set:
        sum = 0
        id = id_set[i]
        for w in q_list:
            if id in tf[w].keys():
                sum += tf[w][id] * idf[w]
        ans[id] = sum / length[id]
    ans = dict(sorted(ans.items(), key = lambda x:x[1], reverse= True))
    j = 0
    for key, value in ans.items():
        if j < K:
            print("{}:{}".format(key, value))
            j += 1
