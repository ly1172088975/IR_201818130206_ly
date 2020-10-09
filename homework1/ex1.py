# -*- coding:utf8 -*
import re
import json
import codecs
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
re_punctuation = "[{}]+".format(punctuation)
'''
f = open("C:/Users/11720/Desktop/IR&DM/EX/E1/tweets.txt", "r", encoding = "utf-8")
f1 = codecs.open("C:/Users/11720/Desktop/IR&DM/EX/E1/dict.txt", "w", encoding = "utf-8")

text_set = {}       #每篇test的内容
id_set = {}         #每篇test的id
i = 1
for lines in f.readlines():
    data = json.loads(lines)
    text_set[i] = data['text']
    id_set[i] = data['tweetId']
    i += 1
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
    for w in w_list:
        if w not in dic:
            #当前索引字典中不存在这个词项
            tmp = set()
            tmp.add(id_set[j])
            dic[w] = tmp
        else:
            dic[w].add(id_set[j])

word_list = dic.items()
sorted(word_list)
for w, id in word_list:
    id_list = list(id)
    id_list.sort()

    #print(w + ':', len(id_list))
    if len(id_list) > 2 :     #词频过低的直接忽略
        f1.write(w + ': ' + str(len(id_list)) + '\n')
        for j in range(0, len(id_list)):
            f1.write(str(id_list[j]) + "  ")
        f1.write('\n')
f1.close()

'''
f = open("C:/Users/11720/Desktop/IR&DM/EX/E1/dict.txt", "r", encoding="utf-8")
dic = {}
k = 0
w = str()
for line in f.readlines():
    if k == 0:
        w = line.split(':')[0]
        #print(w)
    else:
        dic[w] = set(line.split())
        #print(dic)
    k = (k + 1) % 2


while True:
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
    print(q_list)
    ans = set()
    flag = 0
    for j in q_list:
        if j == "and":
            flag = 1
        elif j == "or":
            flag = 2
        elif j == "not":
            flag = 3
        else:
            if j in dic:
                now = dic[j]
            else:
                now = set()
            if flag == 0:
                ans = ans | now
                flag = 4
            elif flag == 2 :
                ans = ans | now
            elif flag == 3:
                ans = ans - now
            else:
                ans = ans & now

    if len(ans) == 0:
        print("not found")
    else:
        ans = list(ans)
        ans.sort()
        for j in range(len(ans)):
            ans[j] = str(ans[j])
        print(", ".join(ans))
        print(len(ans))
