# 实验二：Ranked retrieval model
<br/>
数据集依然是实验一的tweets数据，本文件夹下的dict.txt文件为生成的词项倒排表，记录每个词项的df与在包含它的文档中出现的次数，cnt.txt记录每篇文档的长度（词的个数），ex2.py为本实验源码

<br/>

## 1.读取、整理文本数据信息
该过程与实验一类似，区别在于需要额外记录每个词项在不同文档中的出现次数，此外为了进行最后的cosinescore的计算，需要统计每篇文档的长度，同样加以记录。

<br/>

## 2.计算tf-idf
根据dict.txt和cnt.txt文档来读取相应的数据信息，计算每个词项对应的idf与tf，以及不同文档的长度，其中文档长度length可以直接从cnt.txt中可以查到；df从dict.txt文件中读取，再从原始数据集中统计总文档数，计算idf；tf也从dict.txt文件中读取，取tf=1+log(t)，其中t是词项的词频。具体代码如下：
```python
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
```

<br/>

## 3.查询
查询query处理方法与实验一一样，在对query处理完成后，遍历每一个词项与文档，先计算每个词项与每个文档的相关性，再将query中的词项对应的值加和得到该查询query与每个文档的相关性评分，排序后输出相关性最高的K个文档即可。
```python
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
```
具体查询结果如下：
![image](https://github.com/ly1172088975/IR_201818130206_ly/blob/main/homework2/img.jpg)
<br/>

## 4.总结
本次实验是基于tf-idf的相关性检索模型，考虑到了词项与文本的相关程度进行检索，效果较实验一会更严谨。但tf与idf还有normalization的方法有很多，我只是实现的实验的基本要求，选作部分并没有完成，需要尝试更多的方法来计算结果，这部分内容可以留待以后更新。

<br/>

……待更新……
