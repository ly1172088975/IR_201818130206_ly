# -*- coding: utf-8 -*-
import json
import re
import codecs
import math
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


'''建立索引'''
allset=set()
path1 = "C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E3\\dict.txt"
path2="`C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E3\\`query-res.txt"
f1=codecs.open(path1, 'w', encoding='utf-8')
f = open(r"C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E1\\tweets.txt", "r")
f2 = open(r"C:\\Users\\11720\\Desktop\\IR&DM\\EX\\E3\\query1.txt", "r")
f3=codecs.open(path2, 'w', encoding='utf-8')

punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
re_punctuation = "[{}]+".format(punctuation)

line = f.readline()
docu_set = {}
a = 1
num_set={}
while line:
    dict2 = json.loads(s=line)
    docu_set[a] = dict2['text']
    num_set[a]=dict2['tweetId']
    allset.add(num_set[a])
    a = a + 1
    line = f.readline()
f.close()
n = len(docu_set) + 1
dict1 = dict()  # 定义每一个词所在的所有文档编号
N=len(num_set)
for row in range(1, n):
    information = docu_set[row]
    information = information.lower()
    information = re.sub(re_punctuation, "", information)
    w_list = word_tokenize(information)
    line_words = []
    for w in w_list:
        # w1 = WordNetLemmatizer().lemmatize(w, pos="n")
        w2 = WordNetLemmatizer().lemmatize(w, pos="v")
        w3 = WordNetLemmatizer().lemmatize(w2, pos="a")
        line_words.append(w3)
    for word in line_words:
        if word in dict1:
            if num_set[row] not in dict1[word]:
                dict1[word][num_set[row]]=1
            else:
                dict1[word][num_set[row]]=dict1[word][num_set[row]]+1

        else:
            dict1[word]=dict()
            dict1[word][num_set[row]]=1

'''打印倒排索引'''


word_list = dict1.items()
sorted(word_list)
for key,value in word_list:
    #print(key)
    f1.write('term: '+key+'\n')
    f1.write('DF:'+str(len(dict1[key])))
    f1.write('\n')
    word_list1=value.items()
    sorted(word_list1,key = lambda x:x[0],reverse = True)
    for key1,value1 in word_list1:
        #print(key1+":")
        #print(value1)
        f1.write('tweetid'+key1)
        f1.write('  TF:')
        vv=str(value1)
        f1.write(vv)
        f1.write('\n')
f1.close()

# print(type(word_list))

'''查询'''

query_list = ''
tempset=set()

print("please input the SMART notation of query_tf:"+'\n')
query_tf_notation=input()
print("please input the SMART notation of query_df:"+'\n')
query_df_notation=input()
print("please input the way of Normalization of query:"+'\n')
query_normalization=input()
print("please input the SMART notation of document_tf:"+'\n')
document_tf_notation=input()
print("please input the SMART notation of document_df:"+'\n')
document_df_notation=input()
print("please input the way of Normalization of document:"+'\n')
document_normalization=input()
#print("please input the value of K:"+'\n')
K = 10

li=f2.readline()
while li:
    li=li.replace(',','')
    li=li.replace('.','')
    li=li.replace('"','')
    li=li.replace('-','')
    li = li.split()
    key = li[0]
    value = ''
    for j in range(1, len(li)):
        if j == 1:
            value = li[j]
        else:
            value = value + ' ' + li[j]
    query_list = value
    f3.write(value+'\n')
    print(value)
    docu = dict()  # 储存最后结果
    tf_q = dict()  # 每个term在query中的tf
    tf_d = dict()  # 每个term在该document中的tf
    idf_q = dict()  # 每个term的idf
    idf_d = dict()  # 每个term的idf
    weight_q = dict()  # 最后query得到的tf*idf值
    weight_d = dict()  # 最后document得到的tf*idf值
    query_list = query_list.split()
    for i in range(1, len(num_set)):
        did = num_set[i]
        docu_term = docu_set[i]
        docu_term = docu_term.lower()
        docu_term = re.sub(re_punctuation, "", docu_term)
        w_list = word_tokenize(docu_term)
        line_words = []
        for w in w_list:
            # w1 = WordNetLemmatizer().lemmatize(w, pos="n")
            w2 = WordNetLemmatizer().lemmatize(w, pos="v")
            w3 = WordNetLemmatizer().lemmatize(w2, pos="a")
            line_words.append(w3)
        term_set = set()
        for t in query_list:
            term_set.add(t.lower())
        for t in line_words:
            term_set.add(t)
        '''计算query 的 tf'''
        for te in term_set:
            num = 0
            for ter in query_list:
                if ter == te:
                    num = num + 1
            tf_q[te] = num
        if query_tf_notation == 'n':  # tf=tf
            for i in tf_q:
                tf_q[i] = tf_q[i]
        elif query_tf_notation == 'l':
            for te in term_set:
                num = 0
                for ter in query_list:
                    if ter == te:
                        num = num + 1
                if num == 0:
                    tf_q[te] = 0
                else:
                    tf_q[te] = math.log10(num) + 1
        elif query_tf_notation == 'a':
            maxx = 0
            for te in query_list:
                if maxx < tf_q[te]:
                    maxx = tf_q[te]
            for i in tf_q:
                tf_q[i] = 0.5 + 0.5 * tf_q[i] / maxx
        elif query_tf_notation == 'b':
            for i in tf_q:
                if tf_q[i] > 0:
                    tf_q[i] = 1
                else:
                    tf_q[i] = 0
        elif query_tf_notation == 'L':
            av = 0
            sum = 0
            for te in line_words:
                av = dict1[te][did] + av
                sum = sum + 1
            av = av / sum
            for i in tf_q:
                tf_q[i] = (1 + math.log10(tf_q[i])) / (1 + math.log10(av))
        '''计算idf_query'''
        if query_df_notation == 't':
            for te in term_set:
                if te not in dict1:
                    num=0
                else:
                    num = len(dict1[te])
                if num == 0:
                    idf_q[te] = 0
                else:
                    idf_q[te] = math.log10(N / num)
        elif query_df_notation == 'n':
            for te in term_set:
                idf_q[te] = 1
        elif query_df_notation == 'p':
            for te in term_set:
                num = len(dict1[te])
                if num == 0:
                    idf_q[te] = 0
                else:
                    idf_q[te] = max(0, math.log10((N - num) / num))
        '''计算query的weight'''
        for te in term_set:
            weight_q[te] = idf_q[te] * tf_q[te]
        if query_normalization == 'n':
            for te in term_set:
                weight_q[te] = weight_q[te]
        elif query_normalization == 'c':
            numm = 0
            for te in term_set:
                numm = numm + weight_q[te] * weight_q[te]
            numm = math.sqrt(numm)
            for te in term_set:
                weight_q[te] = weight_q[te] / numm
        # elif query_normalization=='u':
        #
        # elif query_normalization=='b':
        '''计算document的tf'''
        for te in term_set:
            if te not in dict1:
                num=0
            elif did not in dict1[te]:
                num = 0
            else:
                num = dict1[te][did]
            tf_d[te] = num
        if document_tf_notation == 'n':
            for te in term_set:
                tf_d[te] = tf_d[te]
        elif document_tf_notation == 'l':
            for te in term_set:
                if tf_d[te] != 0:
                    tf_d[te] = 1 + math.log10(tf_d[te])
        elif document_tf_notation == 'a':
            maxx = 0
            for te in line_words:
                if maxx < tf_d[te]:
                    maxx = tf_d[te]
            for i in tf_q:
                tf_d[i] = 0.5 + 0.5 * tf_d[i] / maxx
        elif document_tf_notation == 'b':
            for te in term_set:
                if tf_d[te] != 0:
                    tf_d[te] = 1
        elif document_tf_notation == 'L':
            av = 0
            sum = 0
            for te in line_words:
                av = dict1[te][did] + av
                sum = sum + 1
            av = av / sum
            for i in tf_q:
                tf_d[i] = (1 + math.log10(tf_d[i])) / (1 + math.log10(av))
        '''计算document的idf'''
        if document_df_notation == 't':
            for te in term_set:
                num = len(dict1[te])
                if num == 0:
                    idf_d[te] = 0
                else:
                    idf_d[te] = math.log10(N / num)
        elif document_df_notation == 'n':
            for te in term_set:
                idf_d[te] = 1
        elif document_df_notation == 'p':
            for te in term_set:
                num = len(dict1[te])
                if num == 0:
                    idf_d[te] = 0
                else:
                    idf_d[te] = max(0, math.log10((N - num) / num))
        '''计算document（idf为1）的normalization'''
        for te in term_set:
            weight_d[te] = idf_d[te] * tf_d[te]
        if document_normalization == 'n':
            for te in term_set:
                weight_d[te] = weight_d[te]
        elif document_normalization == 'c':
            numm = 0
            for te in term_set:
                numm = numm + weight_d[te] * weight_d[te]
            numm = math.sqrt(numm)
            for te in term_set:
                weight_d[te] = weight_d[te] / numm
        # elif query_normalization=='u':
        #
        # elif query_normalization=='b':
        '''计算该pair的tf_idf'''
        temp = 0
        for te in term_set:
            temp += (weight_q[te] * weight_d[te])
        docu[did] = temp
    '''所有的document计算结束后进行对比'''
    after = dict(sorted(docu.items(), key=lambda e: e[1], reverse=True))
    cnt = 0
    for key, value in after.items():
        cnt += 1
        if cnt > K:
            break
        print("{}:{}".format(key, value))
        f3.write(key+'\n')
    li = f2.readline()